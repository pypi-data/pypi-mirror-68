from typing import Sequence
from typing import Tuple


class OrderedSet(tuple):

    def __new__(cls, iterable):
        """Represents an ordered sequence of unique items.

        The `OrderedSet` implements an immutable ordered sequence of
        unique items.

        Args:
            iterable: An `Iterable`. The items of the set. Must not contain
                duplicates.

        Raises:
            ValueError: If the iterable contains duplicates.

        """

        # The iterable must not contain duplicates.
        if len(set(iterable)) != len(iterable):
            raise ValueError(
                'The iterable must not contain duplicates.')

        self = tuple.__new__(cls, iterable)

        return self

    def __and__(self, *others):
        """Intersection between `OrderedSet`s.

        The intersection of `OrderedSet`s returns a new `OrderedSet` with
        items common to all sets. The items appear in the same order as in the
        first set.

        Args:
            *others: Any number of `OrderedSet`. The other sets to be
                intersected.

        Returns:
            A new instance of `OrderedSet` with the items common to all
            supplied sets.

        """

        variables = []
        for variable in self:
            for other in others:
                if variable not in other:
                    break
            else:
                variables.append(variable)

        return OrderedSet(variables)

    def __eq__(self, other):
        return set(self) == set(other)

    def __ge__(self, other):
        return set(self) >= set(other)

    def __gt__(self, other):
        return set(self) > set(other)

    def __le__(self, other):
        return set(self) <= set(other)

    def __lt__(self, other):
        return set(self) < set(other)

    def __or__(self, other):
        """Union of `OrderedSet`s"""

        # We do not use the set __or__ to preserve order.
        iterable = self + other
        unique = sorted(set(iterable), key=iterable.index)

        return OrderedSet(unique)

    def __ne__(self, other):
        return set(self) != set(other)

    def __sub__(self, item):
        """Subtraction of an item from an `OrderedSet`.

        Args:
            item: An `object`. The item is removed from the set.

        Returns:
            A new `OrderedSet` with the item removed.

        Raises:
            ValueError: If the item is not in the set.

        """

        # If the item is not in the domain, it cannot be removed.
        if item not in self:
            raise ValueError(
                "The item {} is not an item or the set {}."
                .format(item, self))

        return OrderedSet([v for v in self if v != item])


class DiscreteRandomVariable(object):
    def __init__(self, symbol: str, domain: Sequence[object]=None):

        """Represents a discrete random variable in a Bayesian network.

        A `DiscreteRandomVariable` associates a set of possible outcomes
        to a symbol.

        Parameters:
            symbol: The symbol associated with the variable.
            domain: The possible outcomes of the variable. Must not contain
                duplicates.

        Raises:
            ValueError: If the domain contains duplicates.

        Examples:
            A variable representing a coin toss might be created using where 0
            and 1 represent head and tails, respectively.

            >>> coin = DiscreteRandomVariable('coin', (0, 1))
            >>> coin
            coin:(0, 1)

        """

        if domain is None:
            domain = (0, 1)

        if len(set(domain)) != len(domain):
            raise ValueError('The domain contains duplicate outcomes.')

        self._symbol = symbol
        self._domain = tuple(domain)

    @property
    def domain(self) -> Tuple:
        """The possible outcomes of the variable."""
        return self._domain

    @property
    def symbol(self) -> str:
        """The symbol associated with the variable."""
        return self._symbol

    def __len__(self) -> int:
        """The number of possible outcomes of the variable."""
        return len(self._domain)

    def __repr__(self) -> str:
        """Unambiguous string representation of a variable."""
        return '{}:{}'.format(self.symbol, self.domain)
