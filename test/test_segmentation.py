# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestDict:

    def __init__(self):
        self._words = (
            'A',
            'B',
            'CC',
            'AD',
            'AB',
            'E',
            'EA',
        )

    def has_word(self, character_set, text):
        return text in self._words

class TestSegmentation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._dict = TestDict()

    def test_chunking_0(self):
        # List lengtf of 0 should yield a single empty chunk list.
        self.assertEqual([[]], zl.get_chunks('', zl.TRADITIONAL, 0, self._dict, 1, 0))

    def test_chunking_1(self):
        # One character input should yield a single list with one chunk.
        self.assertEqual([['A']], zl.get_chunks('A', zl.TRADITIONAL, 0, self._dict, 1, 1))

    def test_chunking_1(self):
        # List length of 2. Should be ignored because there's not enough input.
        self.assertEqual(
            [['A']],
            zl.get_chunks('A', zl.TRADITIONAL, 0, self._dict, 1, 2)
        )

    def test_chunking_2(self):
        self.assertEqual(
            [['A','A']],
            zl.get_chunks('AA', zl.TRADITIONAL, 0, self._dict, 1, 2)
        )

    def test_chunking_3(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','A']],
            zl.get_chunks('AA', zl.TRADITIONAL, 0, self._dict, 1, 3)
        )

    def test_chunking_4(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','B']],
            zl.get_chunks('AB', zl.TRADITIONAL, 0, self._dict, 1, 3)
        )

    def test_chunking_5(self):
        # List length of 3. Should be ignored because not enough input.
        # Max key length of 2
        self.assertEqual(
            [['A','B'],['AB']],
            zl.get_chunks('AB', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_6(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','CC']],
            zl.get_chunks('ACC', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_7(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','CC', 'B']],
            zl.get_chunks('ACCB', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_8(self):
        self.assertEqual(
            [['A','AD']],
            zl.get_chunks('AAD', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_9(self):
        self.assertEqual(
            [['A','B'], ['AB']],
            zl.get_chunks('AB', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_10(self):
        # Requires a list of length 3.  However, for the second chunk list
        # the input runs out, so it has to return a short list.
        self.assertEqual(
            [['A','E', 'A'], ['A','EA']],
            zl.get_chunks('AEA', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_11(self):
        # This case is different from the previous one because here
        # the required list length of 3 cannot be met because the input
        # does not match rather than the input running out. In this case,
        # there is only one possible chunk list.
        self.assertEqual(
            [['A','E', 'A']],
            zl.get_chunks('AEAXXX', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_12(self):
        # Test when the start of the input has no matching words.
        self.assertEqual(
            [],
            zl.get_chunks('X', zl.TRADITIONAL, 0, self._dict, 1, 1)
        )

    def test_chunking_13(self):
        self.assertEqual(
            [ ['A','B','E'],
              ['A','B','EA'],
              ['AB','E','A'],
              ['AB','EA','A'],
              ['AB','EA', 'AD'] ],
            zl.get_chunks('ABEAAD', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_14(self):
        self.assertEqual(
            [ ['E','A','A'],
              ['E','A','AD'],
              ['EA','AD'] ],
            zl.get_chunks('EAAD', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_15(self):
        self.assertEqual(
            [ ['AD'] ],
            zl.get_chunks('AD', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunk_length(self):
        self.assertEqual(0, zl.chunk_length([]))
        self.assertEqual(3, zl.chunk_length(['AA', 'B']))
        self.assertEqual(6, zl.chunk_length(['AA', 'B', 'CCC']))

    def test_split_into_contiguous(self):
        self.assertEqual(
            ['AB','CD'],
            zl.split_into_contiguous('AB CD')
        )
        self.assertEqual(
            [u'AB',u'CD'],
            zl.split_into_contiguous(u'AB。。CD')
        )
        self.assertEqual(
            [u'AB',u'CD'],
            zl.split_into_contiguous(u'AB。。CD    ')
        )

    def test_segmentation_1(self):
        self.assertEqual(
            ['A'],
            zl.segment('A', zl.TRADITIONAL, self._dict, 2)
        )

    def test_segmentation_2(self):
        self.assertEqual(
            ['AB', 'EA', 'AD'],
            zl.segment('ABEAAD', zl.TRADITIONAL, self._dict, 2)
        )

    def test_segmentation_3(self):
        self.assertEqual(
            ['AB', 'EA', 'AD', 'AB', 'EA', 'AD'],
            zl.segment('ABEAADABEAAD', zl.TRADITIONAL, self._dict, 2)
        )

    def test_segmentation_3(self):
        # Fail because can't match some of it
        with self.assertRaises(zl.DecompositionError) as context_manager:
            zl.segment('ABABXX', zl.TRADITIONAL, self._dict, 2)
        error = context_manager.exception
        self.assertEqual('ABABXX', error.text)

    def test_segmentation_4(self):
        self.assertEqual(
            ['AB', 'EA', 'AD', 'AB', 'EA', 'AD'],
            zl.segment(u'ABEAAD。ABEAAD', zl.TRADITIONAL, self._dict, 2)
        )

    def test_segmentation_5(self):
        self.assertEqual(
            [u'門口',u'水果'],
            zl.segment(u'門口水果', zl.TRADITIONAL)
        )
