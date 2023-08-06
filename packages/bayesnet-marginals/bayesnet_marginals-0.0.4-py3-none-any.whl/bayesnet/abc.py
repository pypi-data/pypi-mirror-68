import operator
from abc import abstractmethod
from functools import reduce
from itertools import product
from typing import Sequence, Generator, Tuple, Iterable

import numpy as np
from recur import Recursive

from bayesnet.core import DiscreteRandomVariable
from bayesnet.core import OrderedSet
from bayesnet.utils import reorder_probabilities


class AbstractProbabilityMassFunction(Recursive):

    def __init__(self, variables: Sequence['DiscreteRandomVariable']):
        """Base class for all implementations of PMF

        The AbstractProbabilityMassFunction is the base class for all
        implementations of PMFs. It manages the variables of the PMF and
        requires that probabilities be accessible, but does not specify
        their implementation.

        Args:
            variables: The variables of the PMFs each having their possible
                states.

        """

        # The variables must all be discrete random variables.
        if not all([isinstance(v, DiscreteRandomVariable) for v in variables]):
            raise TypeError('The variables must be instances of the'
                            'bayesnet.DiscreteRandomVariable class.')

        # The variables are ordered and cannot have duplicates.
        self._variables = OrderedSet(variables)

        # The size of the table if the number of possible outcomes.
        self._size = reduce(operator.mul, (len(v) for v in self.variables))

    @property
    def events(self) -> Generator[Tuple, None, None]:
        """Returns a generator for the events of the PMF."""
        domains = tuple(v.domain for v in self.variables)
        return (e for e in product(*domains))

    @property
    @abstractmethod
    def factored_normalization(self):
        """Returns the normalization as an array of factors"""
        pass

    @property
    @abstractmethod
    def log_normalization(self):
        """Returns the logarithm of normalization coefficient of the PMF"""
        pass

    @property
    def nb_variables(self) -> int:
        """The number of variables of the PMF."""
        return len(self.variables)

    @property
    @abstractmethod
    def normalization(self):
        """Returns the normalization coefficient of the PMF"""
        pass

    @normalization.setter
    @abstractmethod
    def normalization(self, normalization):
        """Sets the normalization coefficient of the PMF"""
        pass

    @property
    @abstractmethod
    def probabilities(self) -> np.ndarray:
        """Returns the probabilities of the PMF

        Returns the probabilities of the PMF, which is a numpy array of
        float with as many elements as there are combinations of states of
        the variables of the PMF.

        """
        pass

    @property
    def size(self) -> int:
        """The number of possible outcomes of the mass function."""
        return self._size

    @property
    def unnormalized(self) -> np.ndarray:
        """The unnormalized probabilities of the PMF."""
        return self.probabilities * self.normalization

    @property
    def variables(self) -> 'OrderedSet[DiscreteRandomVariable]':
        """Returns the variables of the PMF

        Returns the variables of the PMF, which is an immutable ordered set
        of discrete variables.

        """
        return self._variables

    def __contains__(self, variable) -> bool:
        """Indicates if variable is included in the variables of the PMF."""
        return variable in self._variables

    def __eq__(self, other: 'AbstractProbabilityMassFunction'):
        """Indicates if two PMFs are equal.

        Two PMFs are equal if they have the same variables (but not
        necessarily in the same order) and (almost) the same probabilities.

        """

        if self.variables != other.variables:
            return False

        # Reorder the variables so the order matches.
        reordered = reorder_probabilities(self.probabilities,
                                          self.variables, other.variables)
        if not np.all(np.isclose(reordered, other.probabilities)):
            return False

        return True

    def __recur__(self) -> Iterable['AbstractProbabilityMassFunction']:
        """Return the source PMFs. For a pure PMF, there are none."""
        return ()

    def __repr__(self) -> str:
        """Unambiguous string representation for PMFs."""
        return 'PMF over {} with {} events'.format(self.variables, self.size)

    def __str__(self) -> str:
        """Readable string representation for PMFs."""

        out = ''

        # Build the header.
        for variable in self.variables:
            out += '{:<5} '.format(variable.symbol[:5])
        out += '\n'
        out += '------' * self.nb_variables
        out += '----\n'

        # Add the probabilities for each event.
        for probability, event in zip(self.probabilities, self.events):
            for subevent in event:
                out += '{:<5} '.format(subevent)
            out += '{:>4.2f}\n'.format(probability)

        return out


class AbstractProbabilityMassFunctionMarginal(AbstractProbabilityMassFunction):

    def __init__(self, pmf, variable):
        """Base class for all PMF maginals

        In bayesnet, the marginal of a PMF with respect to a variable is
        represented by a class. The AbstractProbabilityMassFunctionMarignal
        class provides the base for all concrete implementations of
        marginals.

        Args:
            pmf: The PMF to marginalize.
            variable: The variable to marginalize out of the PMF.

        """

        # The variable must be in the PMF.
        if variable not in pmf:
            raise ValueError('The variable is not in the PMF.')

        super().__init__(pmf.variables - variable)

        # Keep a reference to the source PMF and variable.
        self._pmf = pmf
        self._variable = variable

    @property
    @abstractmethod
    def normalization(self):
        """Returns the normalization coefficient of the PMF"""
        pass

    @property
    def pmf(self):
        """Returns the source PMF of the marginal"""
        return self._pmf

    @property
    @abstractmethod
    def probabilities(self) -> np.ndarray:
        """Returns the probabilities of the PMF

        Returns the probabilities of the PMF, which is a numpy array of
        float with as many elements as there are combinations of states of
        the variables of the PMF.

        """
        pass

    def __recur__(self) -> Iterable['AbstractProbabilityMassFunction']:
        """Returns the source PMFs of the marginal"""
        return self._pmf,

    @abstractmethod
    def update(self):
        """Updates the probabilities of the PMF marginal"""
        pass


class AbstractProbabilityMassFunctionProduct(AbstractProbabilityMassFunction):

    def __init__(self, left, right):
        """Base class for all PMF product

        In bayesnet, the product of two PMFs is represented by a new class.
        The bayesnet.core.AbstractProbabilityMassFunctionProduct provides
        the base for all concrete implementations of products.

        """

        super().__init__(left.variables | right.variables)

        # Keep a reference to the operands.
        self._left = left
        self._right = right

    @property
    def left(self) -> AbstractProbabilityMassFunction:
        """Returns the left operand of the product"""
        return self._left

    @property
    @abstractmethod
    def probabilities(self) -> np.ndarray:
        """Returns the probabilities of the PMF

        Returns the probabilities of the PMF, which is a numpy array of
        float with as many elements as there are combinations of states of
        the variables of the PMF.

        """
        pass

    @property
    def right(self) -> AbstractProbabilityMassFunction:
        """Returns the right operand of the product"""
        return self._right

    def __recur__(self) -> Iterable['AbstractProbabilityMassFunction']:
        """Returns the source PMFs of the product"""
        return self._left, self._right

    @abstractmethod
    def update(self):
        """Updates the probabilities of the PMF product"""
        pass
