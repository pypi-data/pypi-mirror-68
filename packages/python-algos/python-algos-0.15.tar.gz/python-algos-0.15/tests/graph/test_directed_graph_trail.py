""" Module that contains test for the trail functionality of the directed graph
"""

import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
import os
import time
from pythonalgos.util.logging import Logging
from pythonalgos.util import path_tools as pt
from pythonalgos.util.advisor import Advisor
from os import path

COUNT = "count"


class TestDirectedGraphTrail(unittest.TestCase):

    def setUp(self):
        pass

    def test_trail(self):
        self.vertices = {0: [1, 2], 1: [3, 4], 2: [5, 6, 10], 3: [], 4: [],
                         5: [], 6: [7, 8], 8: [], 7: [9], 9: [2], 10: [11],
                         11: []}
        self.directed_graph = DirectedGraph(self.vertices)
        self.directed_graph.trail(TestAdvisor())
        for edge in self.directed_graph.get_all_edges():
            self.assertEqual(edge.get_attr(COUNT), 1)

    def tearDown(self):
        pass


class TestAdvisor(Advisor):

    def __init__(self):
        super().__init__()

    def visit_vertex(self, directed_graph, vertex):
        print("visited vertex: {0}".format(vertex.get_label()))

    def edge_not_visited(self, directed_graph, edge):
        count = edge.get_attr(COUNT) or 0
        edge.set_attr(COUNT, count + 1)
        print("edge {0}, {1} not visisted".format(edge.get_tail().get_label(),
              edge.get_head().get_label()))

    def edge_visited_already(self, directed_graph, edge):
        print("edge {0}, {1} already visisted".format(edge.get_tail()
              .get_label(), edge.get_head().get_label()))


if __name__ == '__main__':
    unittest.main()
