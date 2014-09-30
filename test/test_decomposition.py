# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

class TestDecomposition(unittest.TestCase):

    def test_decompose_character(self):
        decomposition = zl.decompose(u'好')
        self.assertEquals([u'女', u'子'], decomposition)

    def test_decompose_word(self):
        decomposition = zl.decompose(u'本子')
        self.assertEquals([u'本', u'子'], decomposition)

    def test_decompose_sentence_1(self):
        # Whitespace ignored
        decomposition = zl.decompose(u'本  子')
        self.assertEquals([u'本', u'子'], decomposition)

    def test_decompose_sentence_2(self):
        decomposition = zl.decompose(u'門口好像')
        self.assertEquals([u'門口',u'好像'], decomposition)

if __name__ == '__main__':
    unittest.main()
