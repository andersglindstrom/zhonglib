# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl
import os

class TestDecomposition(unittest.TestCase):

    def test_read_frequency_table(self):
        path = os.path.join(os.path.dirname(__file__), 'test-frequencies.txt')
        table = zl.read_frequency_table(path)
        self.assertEqual(50.0, table['A'])
        self.assertEqual(25.0, table['B'])
        self.assertEqual(12.5, table['C'])

    def test_standard_frequency_table(self):
        self.assertTrue(len(zl._standard_frequency_table) > 0)
        frequency = zl._standard_frequency_table[u'的']
        # Just make sure that it's roughly right.  We're just testing
        # that the file was actually read.
        self.assertTrue(4 < frequency and frequency < 5)
        frequency = zl._standard_frequency_table[u'門']
        frequency = zl._standard_frequency_table[u'门']

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

    def test_decomposition_bug_1(self):
        decomposition = zl.decompose(u'車')
        self.assertEqual([u'二',u'丨',u'日'], decomposition)

    def test_decomposition_bug_2(self):
        decomposition = zl.decompose(u'胖')
        self.assertEqual([u'月', u'半'], decomposition)

    def _test_decomposition_bug_3(self):
        decomposition = zl.decompose(u'中山路')
        self.assertEqual([u'中山', u'路'], decomposition)

    def test_decomposition_bug_4(self):
        decomposition = zl.decompose(u'條')
        self.assertEqual([u'亻', u'丨', u'条'], decomposition)

    def _test_decomposition_bug_5(self):
        decomposition = zl.decompose(u'上星期天')
        self.assertEqual([u'上', u'星期天'], decomposition)

if __name__ == '__main__':
    unittest.main()
