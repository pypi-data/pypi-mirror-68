from bayesnet.abc import AbstractProbabilityMassFunctionProduct
from bayesnet.utils import map_subdomain
from bayesnet.testing import ProbabilityMassFunction
from bayesnet.testing import ProbabilityMassFunctionMarginal

# This module does not provide implementations of PMFs and marginals and uses
# the implementation provided by the testing module. The following two lines,
# which do nothing, are there to stop PyCharm form complaining about unused
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
        self._normalization = None

        self.update()

    @property
    def normalization(self):
        """Returns the normalization coefficient of the PMF"""
        return self._normalization

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

        normalization *= self.left.normalization * self.right.normalization
        self._normalization = normalization
