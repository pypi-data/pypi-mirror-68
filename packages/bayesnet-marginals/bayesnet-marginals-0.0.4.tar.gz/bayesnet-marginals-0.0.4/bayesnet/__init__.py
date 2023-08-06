import json as _json
import os.path as _op
import warnings as _warnings
from typing import Sequence
from typing import Iterable

import bayesnet.base as _base
from bayesnet.abc import AbstractProbabilityMassFunction
from bayesnet.core import DiscreteRandomVariable
from bayesnet.junction import Marginals

# Try to import the OpenCL implementation. Will fail if optional dependencies
# are not installed.
try:
    import bayesnet.opencl as _opencl
except ImportError:
    _opencl = None

# Load the configuration file.
_config_file = _op.join(_op.dirname(__file__), '..', 'config', 'bayesnet.json')
with open(_config_file, 'rt') as f:
    config = _json.load(f)


def _use_opencl() -> bool:

    if config['use-opencl'] and _opencl is not None:
        use_opencl = True
    elif config['use-opencl']:
        _warnings.warn(
            'The configuration indicates that OpenCL should be used, but '
            'pyopencl is not available. Falling back to numpy implementation.')
        use_opencl = False
    else:
        use_opencl = False

    return use_opencl


def pmf(
        variables: Sequence[DiscreteRandomVariable],
        probabilities: Iterable[float] = None,
        normalization: float = None
) -> AbstractProbabilityMassFunction:
    """Returns a new probability mass function"""

    if _use_opencl():
        pmf_class = _opencl.ProbabilityMassFunction
    else:
        pmf_class = _base.ProbabilityMassFunction

    return pmf_class(variables, probabilities, normalization)


def marginals(
        pmfs: Sequence[AbstractProbabilityMassFunction]
) -> Marginals:

    if _use_opencl():
        module = _opencl
    else:
        module = _base

    product_class = module.ProbabilityMassFunctionProduct
    marginal_class = module.ProbabilityMassFunctionMarginal

    return Marginals(pmfs, product_class, marginal_class)
