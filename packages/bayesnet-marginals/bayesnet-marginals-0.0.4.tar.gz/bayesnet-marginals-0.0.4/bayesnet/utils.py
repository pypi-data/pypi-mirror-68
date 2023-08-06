import operator
from functools import reduce
from typing import Sequence

import numpy as np

from bayesnet.core import DiscreteRandomVariable
from bayesnet.core import OrderedSet


def map_subdomain(subdomain: OrderedSet, domain: OrderedSet):
    """Returns a map between two domains"""

    augmented_subdomain = subdomain | domain

    nb_states = tuple(len(v) for v in augmented_subdomain)
    zipped = list(zip(nb_states, augmented_subdomain))
    new_shape = tuple(s if v in subdomain else 1 for s, v in zipped)
    reps = tuple(1 if v in subdomain else s for s, v in zipped)

    size = reduce(operator.mul, (len(v) for v in subdomain))
    subindices = np.tile(np.arange(size).reshape(new_shape), reps)
    new_order = tuple(augmented_subdomain.index(v) for v in domain)

    return subindices.transpose(new_order).ravel()


def reorder_probabilities(
        probabilities: np.ndarray,
        variables: Sequence[DiscreteRandomVariable],
        reordered_variables: Sequence[DiscreteRandomVariable]) \
            -> np.ndarray:
    """Reorders probabilities following a variable reordering

    Reorders an array of probabilities given the original variable order and
    the new variable order.

    Args:
        probabilities: The probabilities to reorder. The number of elements has
            to match the size of the iterable of variables.
        variables: An iterable that contains the variables corresponding to the
            probabilities.
        reordered_variables: An iterable that contains the reordered
            variables. Must contain the same variables as `variables`.

    Examples:

        >>> import numpy as np
        >>> from bayesnet import DiscreteRandomVariable
        >>> from bayesnet.utils import reorder_probabilities

        >>> a = DiscreteRandomVariable('a')
        >>> b = DiscreteRandomVariable('b')
        >>> probabilities = np.array([0.1, 0.2, 0.3, 0.4])

        >>> reorder_probabilities(probabilities, [a, b], [b, a])
        array([0.1, 0.3, 0.2, 0.4])

    """

    # Reorder the probabilities to be able to transpose them.
    shape = tuple(len(v) for v in variables)
    probabilities = probabilities.reshape(shape)

    # Find the permutation that must be applied to the variables and transpose
    # the probabilities.
    order = [variables.index(v) for v in reordered_variables]
    probabilities = probabilities.transpose(order)

    return probabilities.ravel()
