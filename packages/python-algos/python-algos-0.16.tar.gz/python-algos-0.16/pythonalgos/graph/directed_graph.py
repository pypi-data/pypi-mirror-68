from __future__ import annotations
from . vertex import Vertex
from . import kosaraju_sccs
from . import cyclic as cyclic
from . import directed_trail as trail
from . directed_graph_core import DirectedGraphCore
from copy import deepcopy
from .. util.advisor import Advisor
from typing import Any, List, Mapping, Set, Collection
from . edge import Edge
from . algorithm_ordering import AlgorithmOrdering


""" Module that contains the definition of a directed graph as a class """


class DirectedGraph(object):
    """ Class to represent directed graphs.
    https://en.wikipedia.org/wiki/Directed_graph """

    def __init__(self, vertices: Mapping[Any, List[Any]] = None,
                 algorithm_ordering=AlgorithmOrdering.NATURAL):
        """ Initialises a directed graph (with the provided vertices)

        Args:
            vertices(dict): a dict with the vertices and their tails in it
        """

        self.directed_graph = DirectedGraphCore(vertices, algorithm_ordering)

    def copy(self) -> DirectedGraph:
        """ Copies the directed graph and returns it

        Returns:
            the copied directed graph """

        return deepcopy(self)

    def get_vertex(self, label: Any):
        """ Returns the vertex that coincides with the label

        Args:
            label: the label of the vertex

        Returns:
            The vertex object
        """

        return self.directed_graph.get_vertex(label)

    def add_vertex(self, label: Any):
        """ Adds a vertex to the dictionary of vertices

        Args:
            label: a vertex represented by its label """

        self.directed_graph.create_add_vertex(label)

    def get_vertices(self) -> Collection[Vertex]:
        """ Returns the vertices dictionary

        Returns
            self._vertices (dict) """

        return self.directed_graph.get_vertices()

    def add_edge(self, tail: Any, head: Any):
        """ Adds an edge to the graph, the edge is identified by a tail and
        a head vertex.

        Args:
            tail: the edge that represents the start vertex
            head: the edge that represents the destination vertex """

        self.directed_graph.add_edge(tail, head)

    def get_all_edges(self) -> Set[Edge]:
        """ Method that retrieves all edges of all vertices

        Returns:
            set(): A set of all edges in the directed graph """

        return self.directed_graph.get_all_edges()

    def get_vertices_count(self) -> int:
        return self.directed_graph.get_vertices_count()

    def __str__(self):
        return self.directed_graph.__str__()

    def create_sccs_kosaraju_dfs(
            self, nontrivial: bool = True) -> List[Set[Vertex]]:
        return kosaraju_sccs.create_sccs_kosaraju_dfs(self.directed_graph,
                                                      nontrivial)

    def is_cyclic(self, advisor: Advisor = Advisor()):
        """ Method that uses a helper module to check for cycles in the
        directed graph.

        Args:
            advisor(Advisor): The class that implements the advice that is to
            be inserted at join points in the algorith. The default advice is
            empty """

        return cyclic.is_cyclic(self.directed_graph, advisor)

    def trail(self, advisor: Advisor = Advisor()):
        """ Method that trails the directed graph

         Args:
            advisor(Advisor): The class that implements the advice that is to
            be inserted at join points in the algorith. The default advice is
            empty """

        return trail.trail(self.directed_graph, advisor)

    def reversed(self, inplace=True) -> DirectedGraphCore:
        return self.directed_graph.reversed(inplace)

    def get_direct_graph_core(self):
        return self.directed_graph
