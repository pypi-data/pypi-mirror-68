from typing import Sequence
from typing import Iterable

import numpy as np
import pyopencl as cl

from bayesnet import DiscreteRandomVariable
from bayesnet.abc import AbstractProbabilityMassFunction
from bayesnet.abc import AbstractProbabilityMassFunctionMarginal
from bayesnet.abc import AbstractProbabilityMassFunctionProduct
from bayesnet.utils import map_subdomain

# Create the global OpenCL context.
_context = cl.create_some_context(interactive=False)
_queue = cl.CommandQueue(_context)

# Get the number of compute units for the selected device.
_nb_units = _context.devices[0].get_info(cl.device_info.MAX_COMPUTE_UNITS)

# The program used by the marginals.
marginals_program = cl.Program(_context, """
__kernel void isum(__global const float *source,
                   __global const uint *indices,
                   __global float *target,
                   uint nb_states)
{
    uint gid = get_global_id(0);
    uint start = gid * nb_states;

    target[gid] = 0.0;
    for (uint i = start; i < start + nb_states; i++) {
        target[gid] += source[indices[i]];
    }
}
""").build()

product_program = cl.Program(_context, """
__kernel void mul(__global const int *left_map,
                  __global const int *right_map,
                  __global const float *left_data,
                  __global const float *right_data,
                  __global float *result)
{
  int gid = get_global_id(0);
  result[gid] = left_data[left_map[gid]] * right_data[right_map[gid]];
}

__kernel void sum(__global const float *array,
                  __global float *partial_sums,
                  __local float *local_sums)
{
    uint local_id = get_local_id(0);
    uint group_size = get_local_size(0);

    local_sums[local_id] = array[get_global_id(0)];

    for (uint stride = group_size / 2; stride > 0; stride /= 2) {

        barrier(CLK_LOCAL_MEM_FENCE);

        if (local_id < stride) {
            local_sums[local_id] += local_sums[local_id + stride];
        }
    }

    if (local_id == 0) {
        partial_sums[get_group_id(0)] = local_sums[0];
    }
}

__kernel void div(__global float *array,
                  float divisor)
{
    uint global_id = get_global_id(0);
    array[global_id] = array[global_id] / divisor;
}
""").build()


class ProbabilityMassFunction(AbstractProbabilityMassFunction):

    def __init__(self,
                 variables: Sequence[DiscreteRandomVariable],
                 probabilities: Iterable[float] = None,
                 normalization: float = None):
        """Create a new probability mass function."""

        super().__init__(variables)

        # Create a buffer for the probabilities.
        flags = cl.mem_flags.READ_WRITE
        self._buffer = cl.Buffer(_context, flags, size=self.size * 4)

        # The default is to use the same probability for all outcomes.
        if probabilities is None:
            probabilities = np.full((self.size,), 1 / self.size,
                                    dtype=np.float32)
        self.probabilities = probabilities

        # By default, the table is normalized to 1.
        if normalization is None:
            normalization = 1.0

        else:
            if normalization == 0:
                raise ValueError('The normalization coefficient cannot be 0.')
            if np.abs(1 - probabilities.sum()) > 1e-8:
                raise ValueError('To supply a normalization coefficient, '
                                 'the probabilities must be normalized.')

        # The normalization is kept as an array to be able to compute the
        # log normalization without overflow.
        self._normalization: np.ndarray = np.array([normalization])

    @property
    def buffer(self):
        return self._buffer

    @property
    def factored_normalization(self) -> np.ndarray:
        """Returns the normalization as an array of factors"""
        return self._normalization

    @property
    def log_normalization(self):
        """Returns the log of the normalization of the PMF"""
        return np.sum(np.log(self._normalization))

    @property
    def normalization(self) -> float:
        """Get the normalization coefficient of the PMF."""
        return float(np.prod(self._normalization))

    @normalization.setter
    def normalization(self, normalization: float):
        """Set the normalization coefficient of the PMF."""
        self._normalization = np.array([normalization])

    @property
    def probabilities(self):
        probabilities = np.empty((self.size,), dtype=np.float32)
        cl.enqueue_copy(_queue, probabilities, self._buffer)
        return probabilities

    @probabilities.setter
    def probabilities(self, probabilities):

        try:
            probabilities = np.array(probabilities, dtype=np.float32)
        except (TypeError, ValueError):
            raise TypeError('The probabilities must be convertible to a '
                            'numpy array of floats.')

        # The number of probabilities must match the number of outcomes.
        if self.size != probabilities.size:
            raise ValueError('The number of probabilities does not match '
                             'the number of possible outcomes ({} != {}).'
                             .format(self.size, probabilities.size))

        # Copy the new probabilities to the buffer.
        cl.enqueue_copy(_queue, self._buffer, probabilities)


class ProbabilityMassFunctionMarginal(AbstractProbabilityMassFunctionMarginal):

    def __init__(self,
                 pmf: ProbabilityMassFunction,
                 variable: DiscreteRandomVariable):
        """Marginal of a PMF."""

        super().__init__(pmf, variable)

        # Create a buffer for the probabilities.
        flags = cl.mem_flags.READ_WRITE
        self._buffer = cl.Buffer(_context, flags, size=self.size * 4)
        self._index = pmf.variables.index(variable)

        # Generate the source indices of the elements to sum.
        shape = tuple(1 if v is variable else len(v) for v in pmf.variables)
        target_indices = np.arange(self.size).reshape(shape)
        reps = tuple(len(v) if v is variable else 1 for v in pmf.variables)
        tiled_target_indices = np.tile(target_indices, reps)
        indices = np.argsort(tiled_target_indices.ravel()).astype(np.int32)

        # Copy them to the device.
        flags = cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR
        self._indices_buffer = cl.Buffer(_context, flags, hostbuf=indices)

        # Set the program used on the device.
        self._program = marginals_program

        # The normalization is kept as a list to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([1.0])

        # Compute the probabilities.
        self.update()

    @property
    def buffer(self):
        return self._buffer

    @property
    def factored_normalization(self) -> np.ndarray:
        """Returns the normalization as an array of factors"""
        return self._normalization

    @property
    def log_normalization(self):
        """Returns the log of the normalization of the PMF"""
        return np.sum(np.log(self._normalization))

    @property
    def normalization(self):
        """Returns the normalization coefficient of the PMF"""
        return np.prod(self._normalization)

    @property
    def probabilities(self):
        """Returns the probabilities of the PMF"""
        probabilities = np.empty((self.size,), dtype=np.float32)
        cl.enqueue_copy(_queue, probabilities, self._buffer)
        return probabilities

    def update(self):

        # Compute the probabilities on the device.
        self._program.isum(
            _queue, (self.size,), None,
            self._pmf.buffer, self._indices_buffer, self.buffer,
            np.uint32(len(self._variable)))

        self._normalization = self._pmf.factored_normalization.copy()


class ProbabilityMassFunctionProduct(AbstractProbabilityMassFunctionProduct):

    def __init__(self, left, right):
        """A table that is the result of the product of two tables"""

        super().__init__(left, right)

        # Create a buffer for the probabilities.
        flags = cl.mem_flags.READ_WRITE
        self._buffer = cl.Buffer(_context, flags, size=self.size * 4)

        variables = self.variables
        left_map = map_subdomain(left.variables, variables).astype(np.int32)
        right_map = map_subdomain(right.variables, variables).astype(np.int32)

        # Create buffers for both maps.
        flags = cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR
        self._left_map_buffer = cl.Buffer(_context, flags, hostbuf=left_map)
        self._right_map_buffer = cl.Buffer(_context, flags, hostbuf=right_map)

        # Set the program used on the device.
        self._program = product_program

        # The normalization is kept as a list to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([1.0])

        self.update()

    @property
    def buffer(self):
        return self._buffer

    @property
    def factored_normalization(self) -> np.ndarray:
        """Returns the normalization as an array of factors"""
        return self._normalization

    @property
    def normalization(self):
        """Returns the normalization coefficient of the PMF"""
        return np.prod(self._normalization)

    @property
    def log_normalization(self):
        """Returns the log of the normalization of the PMF"""
        return np.sum(np.log(self._normalization))

    @property
    def probabilities(self):
        """Returns the probabilities of the PMF"""
        probabilities = np.empty((self.size,), dtype=np.float32)
        cl.enqueue_copy(_queue, probabilities, self._buffer)
        return probabilities

    def update(self):
        """Updates the result table of the product"""

        # Compute the probabilities on the device.
        self._program.mul(
            _queue, (self.size,), None,
            self._left_map_buffer, self._right_map_buffer,
            self._left.buffer, self._right.buffer, self.buffer)

        # Create a buffer for the probabilities.
        flags = cl.mem_flags.READ_WRITE
        local = min(128, _nb_units)
        nb_partial_sums = int(np.ceil(self.size / local))
        partial_sums_buffer = cl.Buffer(_context, flags, nb_partial_sums * 4)

        work_group_size = (max(1 << (self.size - 1).bit_length(), 4),)
        self._program.sum(
            _queue, work_group_size, (local,),
            self.buffer, partial_sums_buffer, cl.LocalMemory(local * 4)
        )

        partial_sums = np.empty(nb_partial_sums, dtype=np.float32)
        cl.enqueue_copy(_queue, partial_sums, partial_sums_buffer)

        normalization = np.float32(np.sum(partial_sums))
        self._program.div(
            _queue, (self.size,), None, self.buffer, normalization)

        self._normalization = np.hstack((
            [normalization],
            self.left.factored_normalization,
            self.right.factored_normalization))

