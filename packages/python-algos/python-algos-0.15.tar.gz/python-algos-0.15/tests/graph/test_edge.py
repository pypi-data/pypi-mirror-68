""" Module that contains test for the main directed graph functionality
"""

from pythonalgos.graph.directed_graph_core import DirectedGraphCore
import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import Union


class TestEdge(unittest.TestCase):

    def setUp(self):
        self.vertices = {0: [1], 1: [2], 2: []}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_reverse_edge(self):
        vertex0 = self.directed_graph.get_vertex(0)
        vertex1 = self.directed_graph.get_vertex(1)
        vertex2 = self.directed_graph.get_vertex(2)
        edge = vertex1.get_edges()[0]
        edge.reverse()
        self.assertTrue(edge.get_tail() == vertex2)
        self.assertTrue(edge.get_head() == vertex1)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
