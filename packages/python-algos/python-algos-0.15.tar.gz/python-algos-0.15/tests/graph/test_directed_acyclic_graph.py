import unittest
from pythonalgos.graph.directed_acyclic_graph import DirectedAcyclicGraph
import time
from pythonalgos.util.logging import Logging


class TestDirectedAcyclicGraph(unittest.TestCase):

    def test_init_ok(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, 6], 4: [5, 6],
                         5: [], 6: []}
        DirectedAcyclicGraph(self.vertices)
        self.assertTrue(True)

    def test_init_not_ok(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4, 6, 1], 4: [5, 6],
                         5: [], 6: []}
        with self.assertRaises(RuntimeError):
            DirectedAcyclicGraph(self.vertices)

    def test_init_basic_not_ok(self):
        self.vertices = {0: [1], 1: [0]}
        with self.assertRaises(RuntimeError):
            DirectedAcyclicGraph(self.vertices)

    def test_init_basic_ok(self):
        self.vertices = {0: [1], 1: []}
        DirectedAcyclicGraph(self.vertices)

    def test_init_letters(self):
        self.vertices = {"0": ["1"], "1": ["2", "3"], "2": ["3"],
                         "3": ["4", "6"], "4": ["5", "6"],
                         "5": [], "6": []}
        DirectedAcyclicGraph(self.vertices)
        self.assertTrue(True)

    def test_init_booleans(self):
        self.vertices = {True: [False], False: []}
        DirectedAcyclicGraph(self.vertices)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
