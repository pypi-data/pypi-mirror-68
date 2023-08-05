from __future__ import annotations
from . edge import Edge
from typing import List, Mapping, Any, Collection, Set
from . algorithm_ordering import AlgorithmOrdering

""" Module that contains the definition of a vertex in the context of a
directed graph """


class Vertex():
    """ Class to represent details about a vertex in the context of a directed
        graph, being the indegree, outdegree and the tails that are its
        successors. It inherits from the generic Vertex class """

    def __init__(self, label: str,
                 algorithm_ordering=AlgorithmOrdering.NATURAL, **attrs):
        """ Initialises the vertex by adding some specifics

        Args:
            label(str): the label of the vertex
            **attrs: additional attributes that define the vertex
        """

        self._label = label
        self._algorithm_ordering = algorithm_ordering
        self._attrs = attrs
        self._edges: Set[Edge] = set()
        self._indegree = 0

    def add_edge(self, head_vertex: Vertex):
        """ This method adds an edge to the set of edges maintained by the
        vertex

        Args:
            head_vertex: the head vertex to be added

        """

        self._edges.add(Edge(self, head_vertex))

    def set_attr(self, attr: str, value: Any):
        self._attrs[attr] = value

    def get_attr(self, attr: str):
        return self._attrs.get(attr)

    def get_attrs(self) -> Mapping[str, Any]:
        return self._attrs

    def get_label(self) -> str:
        return self._label

    def increase_indegree(self):
        """ This method increases the indegree for the incumbent vertex """
        self._indegree += 1

    def decrease_indegree(self):
        """ This method decreases the indegree for the incumbent vertex """
        self._indegree -= 1

    def get_edge_heads(self) -> List[Vertex]:
        """ Returns the head vertices of the edges of the target vertex """
        return [e.get_head() for e in self.get_edges()]

    def get_edges(self) -> Collection[Edge]:
        """ Returns the edges of a vertex

        Args:
            vertex_sorting: Indicates the ordering of vertices that
                will be used in algorithms where appropriate
        Returns
            self._vertices according to the indicated vertex ordering """

        if self._algorithm_ordering == AlgorithmOrdering.NATURAL:
            return self._edges
        else:
            return sorted(self._edges,
                          key=lambda edge: edge.get_head().get_label(),
                          reverse=self._algorithm_ordering ==
                          AlgorithmOrdering.DESC)

    def remove_edges(self):
        self._edges = set()

    def get_indegree(self) -> int:
        return self._indegree

    def get_outdegree(self) -> int:
        return len(self._edges)

    def __str__(self):
        return str(self.get_label()) + ", outdegree: {}".format(
            self.get_outdegree()) + \
               ", indegree: {}".format(self.get_indegree()) + \
               ", heads: " + ",".join([str(tail.get_label())
                                      for tail in self.get_edge_heads()])
