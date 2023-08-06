from typing import Iterable
from typing import Sequence

import numpy as np

from bayesnet.core import DiscreteRandomVariable
from bayesnet.abc import AbstractProbabilityMassFunction
from bayesnet.abc import AbstractProbabilityMassFunctionMarginal
from bayesnet.abc import AbstractProbabilityMassFunctionProduct
from bayesnet.utils import reorder_probabilities


class ProbabilityMassFunction(AbstractProbabilityMassFunction):

    def __init__(self,
                 variables: Sequence[DiscreteRandomVariable],
                 probabilities: Iterable[float] = None,
                 normalization: float = None):
        """Create a new probability mass function."""

        super().__init__(variables)

        # The default is to use the same probability for all outcomes.
        if probabilities is None:
            probabilities = np.full((self.size,), 1 / self.size,
                                    dtype=np.float64)
        else:
            probabilities = np.array(probabilities, dtype=np.float64)

        # The number of probabilities must match the number of outcomes.
        if self.size != probabilities.size:

            raise ValueError('The number of probabilities does not match '
                             'the number of possible outcomes ({} != {}).'
                             .format(self.size, probabilities.size))

        # By default, the table is normalized to 1.
        if normalization is None:

            normalization = probabilities.sum()
            if normalization == 0:
                raise ValueError('Cannot create a PMF with all 0 '
                                 'probabilities.')
            probabilities /= normalization

        else:
            if normalization == 0:
                raise ValueError('The normalization coefficient cannot be 0.')
            if np.abs(1 - probabilities.sum()) > 1e-8:
                raise ValueError('To supply a normalization coefficient, '
                                 'the probabilities must be normalized.')

        self._probabilities = probabilities

        # The normalization is kept as an array to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([normalization])

    @property
    def factored_normalization(self):
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

    @normalization.setter
    def normalization(self, normalization):
        """Sets the normalization coefficient of the PMF"""
        self._normalization = np.array([normalization])

    @property
    def probabilities(self):
        """Returns the probabilities of the PMF"""
        return self._probabilities

    @probabilities.setter
    def probabilities(self, probabilities):
        self._probabilities = probabilities


class ProbabilityMassFunctionMarginal(AbstractProbabilityMassFunctionMarginal):

    def __init__(self,
                 pmf: ProbabilityMassFunction,
                 variable: DiscreteRandomVariable):
        """Reference implementation for the marginal of a PMF

        The ProbabilityMassFunctionMarginal implements the marginalization
        of a variable from a probability mass function. This implementation is
        provided for testing and reference only.

        Args:
            pmf: The PMF from which we marginalize a variable.
            variable: The variable to marginalize.

        """

        super().__init__(pmf, variable)

        # Pre-compute the output shape of the probabilities.
        self._shape = tuple(len(v) for v in pmf.variables)
        self._index = pmf.variables.index(variable)

        # Reserve space for the probabilities.
        self._probabilities = None

        # The normalization is kept as a list to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([1.0])

        # Compute the probabilities.
        self.update()

    @property
    def factored_normalization(self):
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
        return self._probabilities

    def update(self):
        """Updates the marginal using the current state of the source PMF"""

        # Reshape the probabilities and sum out the variable.
        reshaped = self.pmf.probabilities.reshape(self._shape)
        self._probabilities = np.sum(reshaped, axis=self._index).ravel()
        self._normalization = self.pmf.factored_normalization.copy()


class ProbabilityMassFunctionProduct(AbstractProbabilityMassFunctionProduct):

    def __init__(self, left, right):
        """Reference implementation for the product of PMFs

        The ProbabilityMassFunctionProduct implements the product of two
        probability mass functions. This implementation is inefficient and
        provided for testing and reference only.

        Args:
            left: The left operand of the product.
            right: The right operand of the product.

        """

        super().__init__(left, right)

        probabilities = np.full((self.size,), 1 / self.size, dtype=np.float64)
        self._probabilities = probabilities

        # The normalization is kept as a list to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([1.0])

        self.update()

    @property
    def factored_normalization(self):
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
        return self._probabilities

    def update(self):
        """Updates the probabilities of the product of PMFs"""

        left = self.left
        right = self.right

        # Expand the two tables to contain all variables of the result.
        left_variables = list(left.variables)
        left_tiles = 1
        right_variables = list(right.variables)
        right_tiles = 1
        for variable in self.variables:
            if variable not in left_variables:
                left_variables = [variable] + left_variables
                left_tiles *= len(variable)
            if variable not in right_variables:
                right_variables = [variable] + right_variables
                right_tiles *= len(variable)

        # Reorder the inputs to match the output order.
        left_probabilities = reorder_probabilities(
            np.tile(left.probabilities, (left_tiles,)),
            left_variables,
            self.variables)
        right_probabilities = reorder_probabilities(
            np.tile(right.probabilities, (right_tiles,)),
            right_variables,
            self.variables)

        # Compute the element wise product of probabilities.
        probabilities = left_probabilities * right_probabilities
        normalization = probabilities.sum()
        probabilities /= normalization
        self._probabilities = probabilities

        self._normalization = np.hstack((
            [normalization],
            self.left.factored_normalization,
            self.right.factored_normalization))

