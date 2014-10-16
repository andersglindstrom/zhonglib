# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl
import os

class TestDecomposition(unittest.TestCase):

    def test_read_frequency_table(self):
        path = os.path.join(os.path.dirname(__file__), 'test-frequencies.txt')
        table = zl.read_frequency_table(path)
        self.assertEqual(100, table['A'])
        self.assertEqual(50, table['B'])
        self.assertEqual(25, table['C'])

    def test_standard_frequency_table(self):
        # Just make sure that it's roughly right.  We're just testing
        # that the file was actually read.

        t_frequency = zl.character_frequency(zl.TRADITIONAL, u'門')
        self.assertEqual(89827, t_frequency)

        s_frequency = zl.character_frequency(zl.SIMPLIFIED, u'门')
        self.assertEqual(900, s_frequency)

        # Check the same character has different frequencies in
        # different character sets. Just to make sure that there are
        # actually two different tables.
        t_frequency = zl.character_frequency(zl.TRADITIONAL, u'的')
        self.assertEqual(6538132, t_frequency)

        s_frequency = zl.character_frequency(zl.SIMPLIFIED, u'的')
        self.assertEqual(65535, s_frequency)

    def test_decompose_character(self):
        decomposition = zl.decompose(u'好', zl.TRADITIONAL)
        self.assertEquals([u'女', u'子'], decomposition)

    def test_decompose_word(self):
        decomposition = zl.decompose(u'本子', zl.TRADITIONAL)
        self.assertEquals([u'本', u'子'], decomposition)

    def test_decompose_sentence_1(self):
        # Whitespace ignored
        decomposition = zl.decompose(u'本  子', zl.TRADITIONAL)
        self.assertEquals([u'本', u'子'], decomposition)

    def test_decompose_sentence_2(self):
        decomposition = zl.decompose(u'門口好像', zl.TRADITIONAL)
        self.assertEquals([u'門口',u'好像'], decomposition)

    def test_decomposition_bug_1(self):
        decomposition = zl.decompose(u'車', zl.TRADITIONAL)
        self.assertEqual([u'二',u'丨',u'日'], decomposition)

    def test_decomposition_bug_2(self):
        decomposition = zl.decompose(u'胖', zl.TRADITIONAL)
        self.assertEqual([u'月', u'半'], decomposition)

    def test_decomposition_bug_3(self):
        # The following exercises the morphic freedom rule.
        decomposition = zl.decompose(u'中山路', zl.TRADITIONAL)
        # This isn't actually what we want but it's what the algorithm gives
        # us from the frequencies. The morphic
        self.assertEqual([u'中', u'山路'], decomposition)

    def test_decomposition_bug_4(self):
        decomposition = zl.decompose(u'條', zl.TRADITIONAL)
        self.assertEqual([u'亻', u'丨', u'条'], decomposition)

    def test_decomposition_bug_5(self):
        # This example exercises the morphic freedom rule, which used not
        # to be implemented.
        decomposition = zl.decompose(u'上星期天', zl.TRADITIONAL)
        self.assertEqual([u'上', u'星期天'], decomposition)

    def test_decomposition_bug_6(self):
        # This example exercises the morphic freedom rule, which used not
        # to be implemented.
        decomposition = zl.decompose(u'爱情', zl.SIMPLIFIED)
        self.assertEqual([u'爱',u'情'], decomposition)

    def test_decomposition_bug_7(self):
        # Should ignore non-Chinese characters.
        decomposition = zl.decompose(u'1. 你好', zl.SIMPLIFIED)
        self.assertEqual([u'你',u'好'], decomposition)

if __name__ == '__main__':
    unittest.main()
