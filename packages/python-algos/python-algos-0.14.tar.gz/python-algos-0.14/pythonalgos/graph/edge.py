from typing import Mapping, Any

""" Module that contains the definition of the class that represents an edge in
a directed graph
"""


class Edge(object):
    """ Class that represents an edge in a directed graph. An edge is
    characterized by a tail, a head and a set of attributes.

    The attributes can be anything that the implementation is interested in.
    For example, a weighted graph would have a necessity to put a weight to
    each edge."""

    def __init__(self, tail, head, **attrs: Mapping[str, str]):
        """ Initialises the edge.

        Args:
            tail(Vertex): the tail vertex
            head(Vertex): the head vertex
            **attrs: additional atttributes that define the edge
        """

        self._label = None
        self._tail = tail
        self._head = head
        self._attrs = attrs

    def get_tail(self):
        return self._tail

    def get_head(self):
        return self._head

    def set_tail(self, tail):
        self.tail = tail

    def set_head(self, head):
        self.head = head

    def set_attr(self, attr: str, value: Any):
        self._attrs[attr] = value

    def reverse(self):
        self._tail, self._head = self._head, self._tail

    def get_attr(self, attr: str) -> Any:
        return self._attrs.get(attr)
