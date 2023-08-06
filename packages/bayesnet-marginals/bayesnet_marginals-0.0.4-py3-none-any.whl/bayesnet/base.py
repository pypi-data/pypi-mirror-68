import numpy as np

from bayesnet.abc import AbstractProbabilityMassFunctionProduct
from bayesnet.utils import map_subdomain
from bayesnet.testing import ProbabilityMassFunction
from bayesnet.testing import ProbabilityMassFunctionMarginal

# This module does not provide implementations of PMFs and marginals and uses
# the implementation provided by the testing module. The following two lines,
# which do nothing, are there to stop PyCharm from complaining about unused
# imports.
ProbabilityMassFunction = ProbabilityMassFunction
ProbabilityMassFunctionMarginal = ProbabilityMassFunctionMarginal


class ProbabilityMassFunctionProduct(AbstractProbabilityMassFunctionProduct):

    def __init__(self, left, right):
        """A table that is the result of the product of two tables"""

        super().__init__(left, right)

        self._left_map = map_subdomain(left.variables, self.variables)
        self._right_map = map_subdomain(right.variables, self.variables)

        # Add the private attributes. Their value is assigned during the
        # update.
        self._probabilities = None

        # The normalization is kept as a list to be able to compute the
        # log normalization without overflow.
        self._normalization = np.array([1.0])

        self.update()

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
        return self._probabilities

    def update(self):
        """Updates the result table of the product"""

        # Reorder the probabilities using the map and compute the product.
        probabilities = \
            self.left.probabilities[self._left_map] * \
            self.right.probabilities[self._right_map]

        normalization = probabilities.sum()
        probabilities /= normalization
        self._probabilities = probabilities

        self._normalization = np.hstack((
            [normalization],
            self.left.factored_normalization,
            self.right.factored_normalization))

