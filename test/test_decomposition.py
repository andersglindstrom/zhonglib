# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

class TestDecomposition(unittest.TestCase):

    def test_decompose_word_1(self):
        decomposition = zl.decompose(u'好')
        self.assertEquals([u'女', u'子'], decomposition)

    def test_decompose_word_2(self):
        decomposition = zl.decompose(u'本子')
        self.assertEquals([u'本', u'子'], decomposition)

if __name__ == '__main__':
    unittest.main()
