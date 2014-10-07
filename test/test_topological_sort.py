# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

class TestTopologicalSort(unittest.TestCase):

    def test_1(self):
        graph = {'A':[]}
        result = zl.topological_sort(graph)
        self.assertEqual(['A'], result)

    def test_1_2(self):
        graph = {'A':['B'], 'B':[]}
        result = zl.topological_sort(graph)
        self.assertEqual(['B', 'A'], result)

    def test_2(self):
        graph = {'A':['B', 'D'], 'B':['C'], 'C':['D'], 'D':[]}
        result = zl.topological_sort(graph)
        self.assertEqual(['D', 'C', 'B', 'A'], result)

    def test_3(self):
        graph = {'A':['B', 'C'], 'B':['D'], 'C':['D'], 'D':[]}
        result = zl.topological_sort(graph)
        self.assertEqual('D', result[0])
        self.assertEqual('A', result[3])
        # 'B' and 'C' must be in result[1] and result[2] but we don't
        # care about the order.

    def test_4(self):
        graph = {'A':['B', 'E'], 'B':['C', 'E'], 'C':['D', 'E'], 'D':['E'], 'E':[]}
        result = zl.topological_sort(graph)
        self.assertEqual(['E', 'D', 'C', 'B', 'A'], result)

    def test_cycle(self):
        graph = {'A':['B'], 'B':['C'], 'C':['A']}
        with self.assertRaises(zl.ZhonglibException) as cm:
            result = zl.topological_sort(graph)
        self.assertEqual('The graph has a cycle.', cm.exception.message)
