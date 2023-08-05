""" Module thatAlgorithmOrderfor the main directed graph functionality
"""

from pythonalgos.graph.algorithm_ordering import AlgorithmOrdering
import unittest
from pythonalgos.graph.directed_graph import DirectedGraph


class TestEdge(unittest.TestCase):

    def setUp(self):
        self.vertices = {0: [1], 1: [2], 2: [], 3: [6, 5, 4], 6: [],
                         5: [], 4: []}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_reverse_edge(self):
        vertex1 = self.directed_graph.get_vertex(1)
        vertex2 = self.directed_graph.get_vertex(2)
        edge = next(iter(vertex1.get_edges()))
        edge.reverse()
        self.assertTrue(edge.get_tail() == vertex2)
        self.assertTrue(edge.get_head() == vertex1)

    def test_get_edges_ascending_order(self):
        self.directed_graph = DirectedGraph(
            self.vertices, algorithm_ordering=AlgorithmOrdering.ASC)
        self.assertTrue(next(iter(
            self.directed_graph.get_vertex(3).get_edges()))
                .get_head().get_label() == 4)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
