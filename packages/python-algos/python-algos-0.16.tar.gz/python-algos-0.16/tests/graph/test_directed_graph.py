""" Module that contains test for the main directed graph functionality
"""

from pythonalgos.graph.algorithm_ordering import AlgorithmOrdering
from pythonalgos.graph.directed_graph_core import DirectedGraphCore
import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import Union


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 5: [5], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_init(self):
        self.assertEqual(len(self.vertices.keys()),
                         self.directed_graph.get_vertices_count())

    def test_str(self):
        print(self.directed_graph)

    def test_one_vertex_self_loop(self):
        self.vertices = {0: [0]}
        self.directed_graph = DirectedGraph(self.vertices)

    def test_add_vertex(self):
        label = 7
        self.directed_graph.add_vertex(label)
        vertex = self.directed_graph.get_vertex(label)
        self.assertIsNotNone(vertex)
        self.assertEqual(vertex.get_outdegree(), 0)
        self.assertEqual(vertex.get_indegree(), 0)
        self.assertListEqual(vertex.get_edge_heads(), list())

    def test_add_duplicate_vertex(self):
        label = 7
        self.directed_graph.add_vertex(label)
        with self.assertRaises(RuntimeError):
            self.directed_graph.add_vertex(label)

    def test_add_heads(self):
        vertex_to_test = 7
        self.directed_graph.add_vertex(vertex_to_test)
        vertex = self.directed_graph.get_vertex(vertex_to_test)
        no_heads = 3
        for i in range(no_heads):
            vertex.add_edge(self.directed_graph.get_vertex(i))
        self.assertEqual(len(vertex.get_edge_heads()), no_heads)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_edge_heads()))

    def test_outdegree(self):
        vertex = self.directed_graph.get_vertex(1)
        self.assertEqual(vertex.get_outdegree(), len(vertex.get_edge_heads()))

    def test_indegree(self):
        vertex_to_test = 6
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, vertex_to_test],
                         4: [5, vertex_to_test], 5: [5], vertex_to_test: []}
        self.directed_graph = DirectedGraph(self.vertices)
        vertex = self.directed_graph.get_vertex(vertex_to_test)
        self.assertEqual(vertex.get_indegree(), 2)

    def test_get_reversed_graph(self):
        self.directed_graph = DirectedGraph(self.vertices)
        self.directed_graph.reversed(inplace=True)
        self.check_big_reversed_graph(self.directed_graph)

    def test_get_reversed_small_graph_inplace_false(self):
        self.vertices = {0: [1], 1: [2], 2: []}
        self.directed_graph = DirectedGraph(self.vertices)
        reversed_graph = self.directed_graph.reversed(inplace=False)
        self.assertTrue(reversed_graph !=
                        self.directed_graph.get_direct_graph_core())
        self.check_small_reversed_graph(reversed_graph)

    def test_get_reversed_small_graph_inplace_true(self):
        self.vertices = {0: [1], 1: [2], 2: []}
        self.directed_graph = DirectedGraph(self.vertices)
        reversed_graph = self.directed_graph.reversed(inplace=True)
        self.assertTrue(reversed_graph ==
                        self.directed_graph.get_direct_graph_core())
        self.check_small_reversed_graph(reversed_graph)

    def test_ordering(self):
        self.vertices = {5: [5], 1: [2, 3], 2: [3],
                         3: [4, 6], 4: [5, 6], 0: [1], 6: [6]}
        self.directed_graph = DirectedGraph(self.vertices,
                                            AlgorithmOrdering.ASC)
        self.assertTrue(next(iter(
            self.directed_graph.get_vertices())).get_label() == 0)

        self.directed_graph = DirectedGraph(self.vertices,
                                            AlgorithmOrdering.DESC)
        self.assertTrue(next(iter(
            self.directed_graph.get_vertices())).get_label() == 6)

    def tearDown(self):
        pass

    def check_small_reversed_graph(self, reversed_graph):
        self.assertTrue(self.amount_of_tails2(reversed_graph, 2) == 1)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 2, 1))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 1) == 1)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 1, 0))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 0) == 0)

    def check_big_reversed_graph(self, reversed_graph):
        self.assertTrue(self.amount_of_tails2(reversed_graph, 6) == 3)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 6, 4))
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 6, 6))
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 6, 3))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 5) == 2)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 5, 5))
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 5, 4))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 4) == 1)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 4, 3))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 3) == 2)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 3, 1))
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 3, 2))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 2) == 1)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 2, 1))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 1) == 1)
        self.assertTrue(self.has_vertex_label_as_head2(reversed_graph, 1, 0))
        self.assertTrue(self.amount_of_tails2(reversed_graph, 0) == 0)

    def has_vertex_label_as_head(
            self,
            graph: DirectedGraphCore,
            vertex_label: Union[str, int],
            head_label: Union[str, int]) -> bool:
        return True if head_label in \
            {v.get_label() for v in
                graph.get_vertex(vertex_label).get_edge_heads()} \
            else False

    def amount_of_heads(
            self,
            graph: DirectedGraphCore,
            vertex_label: Union[str, int]) -> int:
        return len(graph.get_vertex(vertex_label).get_edge_heads())

    def has_vertex_label_as_head2(
            self,
            graph: DirectedGraph,
            vertex_label: Union[str, int],
            head_label: Union[str, int]) -> bool:
        return True if head_label in \
            {v.get_label() for v in
                graph.get_vertex(vertex_label).get_edge_heads()} \
            else False

    def amount_of_tails2(
            self,
            graph: DirectedGraph,
            vertex_label: Union[str, int]) -> int:
        return len(graph.get_vertex(vertex_label).get_edge_heads())


if __name__ == '__main__':
    unittest.main()
