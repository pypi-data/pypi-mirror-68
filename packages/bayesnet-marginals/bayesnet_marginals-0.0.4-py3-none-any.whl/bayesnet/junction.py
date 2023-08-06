from functools import reduce
from itertools import combinations
from typing import Callable, List, Sequence, Set, Tuple

import numpy as np

from recur.abc import descendants, MultiRecursive, Recursive
from recur.abc import preorder, postorder

from bayesnet.core import DiscreteRandomVariable
from bayesnet.base import ProbabilityMassFunction
from bayesnet.base import ProbabilityMassFunctionMarginal
from bayesnet.base import ProbabilityMassFunctionProduct


class JunctionTreeNode(MultiRecursive):
    def __init__(self,
                 variables: Set[DiscreteRandomVariable],
                 boundary: Set[DiscreteRandomVariable],
                 tables: Sequence[ProbabilityMassFunction]):
        """A node in a junction tree

        A junction tree is a data structure that allows fast computation of
        the marginals of a Bayesian network. The JunctionTreeNode class
        represents a node in this data structure.

        Args:
            variables: All the variables of the node.
            boundary: The variables that have links to over variables in the
                tree.
            tables: The sequence of probability mass functions of the node.

        """

        super().__init__()
        self.variables = variables
        self.boundary = boundary
        self.tables = tables
        self.collect = None
        self.distribute = None

        self._children = []
        self._parent = None

    @property
    def children(self) -> List['JunctionTreeNode']:
        """Returns the children of the current node"""
        return self._children

    @property
    def parent(self) -> 'JunctionTreeNode':
        """Returns the parent of the current node"""
        return self._parent

    def __multirecur__(self, index):
        """Iteration over descendants or ancestors of the node"""

        # Iterate over descendants (0) or ancestors (1).
        if index == 0:
            return self._children
        elif index == 1:
            return [] if self._parent is None else [self._parent]

    def add(self, child: 'JunctionTreeNode'):
        """Adds a child to the current node

        When adding a child, two links are created. One from the parent (self)
        to the child and one from the child to the parent. To prevent loops,
        child cannot already have a parent.

        Args:
            child: The new child of the current node.

        Raises:
            ValueError: If the child already has a parent.

        """

        if child._parent is not None:
            raise ValueError('The junction tree node already belong to '
                             'another junction tree.')

        self._children.append(child)
        child._parent = self


def construct_junction_trees(tables: Sequence[ProbabilityMassFunction]) \
        -> List[JunctionTreeNode]:
    """Constructs a junction trees from PMFs

    Returns a list of junction trees created from a list of probability mass
    functions.

    Args:
         tables: The sequence of PMFs.

    Returns:
        trees: A list of junction trees.

    """

    remaining_tables = tables

    trees = []
    nb_nodes_removed = 0

    # There will be one junction tree per moral graph.
    for graph in moral_graphs(tables):

        nodes = []
        while graph is not None:

            # Find a the node with the lowest number of missing
            # neighbors.
            node = graph.minimize(lambda n: n.nb_missing_links)

            # If the node is not simplicial, add the missing links.
            if not node.is_simplicial:
                for n1, n2 in combinations(node.neighbors, 2):
                    n1.add(n2)

            family = node.family
            boundary = node.boundary
            to_remove = family - boundary

            # Get the tables that contain the nodes to remove.
            vars_to_remove = set(n.variable for n in to_remove)
            node_tables = [t for t in remaining_tables
                           if len(vars_to_remove & set(t.variables)) != 0]
            remaining_tables = [t for t in remaining_tables
                                if t not in node_tables]

            # Remove the nodes that are not on the boundary.
            nb_nodes_removed = nb_nodes_removed + len(to_remove)
            for node in to_remove:
                node.remove()

            nodes.append(JunctionTreeNode(
                set(n.variable for n in family),
                set(n.variable for n in boundary),
                node_tables))
            graph = next((n for n in boundary), None)

        for i, child in enumerate(nodes):
            for parent in nodes[i + 1:]:
                if child.boundary <= parent.variables:
                    parent.add(child)
                    break

        trees.append(nodes[-1])

    return trees


class Marginals(object):
    def __init__(
            self,
            pmfs: Sequence[ProbabilityMassFunction],
            product_class: Callable = ProbabilityMassFunctionProduct,
            marginal_class: Callable = ProbabilityMassFunctionMarginal):
        """Marginals of a Bayesian network

        The Marginals class computes the marginals of all the variables of a
        Bayesian network described by a sequence of PMFs. If the input PMFs
        change, the marginals can be updated efficiently.

        Args:
            pmfs: The sequence of PMFs describing the Bayesian network.

        """

        self._pmfs = pmfs

        # Generate the junction tree of the Bayesian network.
        junction_trees = construct_junction_trees(pmfs)

        # Compute the marginals for each tree.
        update_list = []
        marginals = []
        independent_marginals = []
        for junction_tree in junction_trees:
            update_list += _collect(
                junction_tree, product_class, marginal_class)
            update_list += _distribute(
                junction_tree, product_class, marginal_class)
            local_marginals, marginals_update_list = _marginals(
                junction_tree, product_class, marginal_class)
            marginals += local_marginals
            independent_marginals.append(local_marginals)
            update_list += marginals_update_list

        self._marginals = marginals
        self._independent_marginals = independent_marginals
        self._update_list = update_list

        # Get the order of the variables for quick access.
        self._variables = [m.variables[0] for m in marginals]

    @property
    def normalization(self):
        """Returns the normalization coefficient of all marginals"""
        return np.prod([m[0].normalization
                        for m in self._independent_marginals])

    @property
    def log_normalization(self):
        """Returns the log of the normalization coefficient of all marginals"""
        return np.sum([m[0].log_normalization
                       for m in self._independent_marginals])

    def __getitem__(self, item):
        """Get a specific marginal"""
        return self._marginals[self._variables.index(item)]

    def update(self):
        """Recompute the marginals using updated PMFs"""
        for pmf in self._update_list:
            pmf.update()


class MoralGraphNode(Recursive):
    def __init__(self, variable: DiscreteRandomVariable):
        """A node of a moral graph

        A moral graph is the undirected form of a directed acyclic graph
        i.e. a Bayesian network. It is used to generate the junction tree
        of a Bayesian network.

        Args:
            variable: The variable contained in the node.

        """

        super().__init__()
        self._variable = variable
        self._neighbors = set()

    def __recur__(self):
        """Iterate over the neighbors of the node"""
        return self._neighbors

    @property
    def boundary(self) -> Set['MoralGraphNode']:
        """Get the boundary of a node

        The boundary is the set of nodes that are in the neighborhood of a
        node, but adjacent to nodes not in the neighborhood.

        """

        family = self.family
        output = set()
        for neighbor in self.neighbors:
            if not neighbor.neighbors <= family:
                output.add(neighbor)

        return output

    @property
    def family(self) -> Set['MoralGraphNode']:
        """Get the family of a node"""

        return set(self._neighbors) | {self}

    @property
    def is_simplicial(self) -> bool:
        """Indicates if a node is simplicial

        A node is simplicial if all the nodes it is linked to are pairwise
        linked. In other words, the family of the node form a clique.

        """

        for node, other_node in combinations(self.neighbors, 2):
            if node not in other_node.neighbors:
                return False

        return True

    @property
    def nb_missing_links(self) -> int:
        """Counts the number of missing links to make the node simplicial"""

        missing = 0
        for node, other_node in combinations(self.neighbors, 2):
            if node not in other_node.neighbors:
                missing += 1

        return missing

    @property
    def neighbors(self) -> Set['MoralGraphNode']:
        """Returns the neighbors of the node"""
        return self._neighbors

    @property
    def variable(self) -> DiscreteRandomVariable:
        """Returns the variable of the node"""
        return self._variable

    def add(self, other: 'MoralGraphNode'):
        """Add another node as a neighbor"""
        self._neighbors.add(other)
        other._neighbors.add(self)

    def minimize(self, cost: Callable) -> 'MoralGraphNode':
        """Find the node that minimize a cost function"""
        return min(((n, cost(n)) for n in self), key=lambda v: v[1])[0]

    def remove(self):
        """Removes a node from a graph"""

        # Remove the links from the neighbors to the node.
        for neighbor in self.neighbors:
            neighbor._neighbors.remove(self)

        # Remove the links from the node to the neighbors.
        self._neighbors = set()


def moral_graphs(pmfs) -> List[MoralGraphNode]:
    """Builds the moral graph or graphs from a list of PMFs

    Builds one or many moral graphs from a list of probability mass
    functions. The number of graphs returned depends on the number of
    disconnected graphs represented by the tables.

    Args:
        pmfs: The sequence of probability mass functions used to build
            the moral graphs.

    """

    # Get the unique variables of the graph and create a node for
    # each of them.
    variables = list(set(v for pmf in pmfs for v in pmf.variables))
    nodes = [MoralGraphNode(v) for v in variables]

    # Add the links between nodes. Because the nodes are undirected, every add
    # creates a symmetric link.
    for pmf in pmfs:
        for n1, n2 in combinations(pmf.variables, 2):
            nodes[variables.index(n1)].add(nodes[variables.index(n2)])

    # It is possible for tables to generate disconnected graphs. Here we
    # select one node for every one.
    graphs = []
    while len(nodes) > 0:
        graphs.append(nodes[0])
        for node in graphs[-1]:
            nodes.remove(node)

    return graphs


def _collect(
        junction_tree: JunctionTreeNode,
        product_class: Callable = ProbabilityMassFunctionProduct,
        marginal_class: Callable = ProbabilityMassFunctionMarginal,) \
        -> List['ProbabilityMassFunction']:
    """Collects the information of the junction tree

    Collects the information of the junction tree by passing the information
    from the child nodes to their parents.

    Args:
        junction_tree: The root node of the junction tree.

    Returns:
        update_list: The list of PMFs that must be updated to "recollect"
            the junction tree when the input PMFs change.

    """

    update_list = []

    def product(left, right):
        new_table = product_class(left, right)
        update_list.append(new_table)
        return new_table

    for node in postorder(descendants(junction_tree)):

        if node.parent is not None:

            # Get the tables of the current node and the collect ones
            # from its children.
            tables = node.tables + [n.collect for n in node.children]

            # Marginalize all variables that are not in the boundary.
            for variable in node.variables - node.boundary:

                # Get the tables that contain the variable to marginalize.
                subtables = [t for t in tables if variable in t]

                # If there is more that one, collapse it.
                if len(subtables) > 1:
                    subtable = reduce(product, subtables)
                else:
                    subtable = subtables[0]

                marginal = marginal_class(subtable, variable)
                update_list.append(marginal)

                tables = [t for t in tables if variable not in t] + \
                         [marginal]

            # It is possible to have many left over tables depending on the
            # order of evaluation. Reduce them to one.
            if len(tables) > 1:
                table = reduce(product, tables)
                update_list.append(table)
                node.collect = table
            else:
                node.collect = tables[0]

    return update_list


def _distribute(
        junction_tree: JunctionTreeNode,
        product_class: Callable = ProbabilityMassFunctionProduct,
        marginal_class: Callable = ProbabilityMassFunctionMarginal,) \
        -> List[ProbabilityMassFunction]:
    """Distributes the information of the junction tree

    Distributes the information in the junction tree by passing information
    from the parent nodes to the child nodes. _collect should always be
    called before _distribute.

    Args:
        junction_tree: The root node of the junction tree.

    Returns:
        update_list: The PMFs that must be updated to redistribute the
            junction tree if the source PMF change.

    """

    update_list = []

    def product(left, right):
        new_table = product_class(left, right)
        update_list.append(new_table)
        return new_table

    for node in preorder(descendants(junction_tree)):

        for child in node.children:

            # Get the table from the node, the distribute table from the
            # parent, and the collect tables from the children.
            children = (c for c in node.children if c is not child)
            tables = node.tables + [c.collect for c in children]

            if node.distribute is not None:
                tables.append(node.distribute)

            # Marginalize all variables that are not in the boundary of
            # the child.
            for variable in node.variables - child.boundary:

                # Get the tables that contain the variable to marginalize.
                subtables = [t for t in tables if variable in t]

                # If there is more than one, collapse it.
                if len(subtables) > 1:
                    subtable = reduce(product, subtables)
                else:
                    subtable = subtables[0]

                marginal = marginal_class(subtable, variable)
                update_list.append(marginal)

                tables = [t for t in tables if variable not in t] + \
                         [marginal]

            # It is possible to have many left over tables depending on the
            # order of evaluation. Reduce them to one.
            if len(tables) > 1:
                table = reduce(product, tables)
                update_list.append(table)
                child.distribute = table
            else:
                child.distribute = tables[0]

    return update_list


def _marginals(
        junction_tree: JunctionTreeNode,
        product_class: Callable = ProbabilityMassFunctionProduct,
        marginal_class: Callable = ProbabilityMassFunctionMarginal) \
        -> Tuple[List[ProbabilityMassFunction], List[ProbabilityMassFunction]]:
    """Computes the marginals of a junction tree

    Computes a marginal for each variable of a junction tree. Also generates
    the update list needed to update the marginals if the input PMFs change.
    _collect and _distribute need to be called before _marginals.

    Args:
        junction_tree: The root node of the junction tree.

    Returns:
        marginals: The list of marginals for each variable of the junction
            tree.
        update_list: The PMFs that need to be updated to recompute the
            marginals.
    """

    marginals = []
    update_list = []
    visited = set()

    def product(left, right):
        new_table = product_class(left, right)
        update_list.append(new_table)
        return new_table

    for node in preorder(descendants(junction_tree)):

        # If the node contains variables we have not seen yet, compute their
        # marginal
        new_variables = node.variables - node.boundary - visited
        if len(new_variables) > 0:

            visited |= new_variables

            # Collect all the relevant PMFs
            tables = node.tables + [c.collect for c in node.children]
            if node.distribute is not None:
                tables.append(node.distribute)

            # Collapse them to a single table.
            if len(tables) > 1:
                table = reduce(product, tables)
            else:
                table = tables[0]

            # Compute the marginal for each new variable.
            for variable in new_variables:

                marginal = table
                for to_marginalize in node.variables - {variable}:
                    marginal = marginal_class(marginal, to_marginalize)
                    update_list.append(marginal)

                marginals.append(marginal)

    return marginals, update_list
