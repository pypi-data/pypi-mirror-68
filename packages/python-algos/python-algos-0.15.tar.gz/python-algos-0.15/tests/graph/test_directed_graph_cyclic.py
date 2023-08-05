""" Module that contains test for the cyckic checking functionality of the
directed graph """

import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
import os
import time
from pythonalgos.util.logging import Logging
from pythonalgos.util import path_tools as pt
from os import path


class TestDirectedGraphCyclic(unittest.TestCase):

    def setUp(self):
        pass

    def test_cyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [3],
                         3: [4], 4: [5, 2], 5: [6], 6: [7], 7: [5]}
        self.directed_graph = DirectedGraph(self.vertices)
        self.assertTrue(self.directed_graph.is_cyclic())

    def test_acyclic(self):
        Logging.enable()
        self.vertices = {0: [1], 1: [2, 3], 2: [
            3], 3: [4, 6], 4: [5, 6], 5: [], 6: []}
        self.directed_graph = DirectedGraph(self.vertices)
        self.assertFalse(self.directed_graph.is_cyclic())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
