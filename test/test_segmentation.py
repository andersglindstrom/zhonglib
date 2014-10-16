# -*- coding: utf-8 -*-

import os
import os.path
import unittest
import zhonglib as zl

class TestDict:

    def __init__(self):
        self._words = (
            u'阿', # A
            u'比', # B
            u'西西', # CC
            u'阿地', # AD
            u'阿比', # AB
            u'一',  # E
            u'一阿', # EA
            u'A',
            u'B',
            u'CC',
            u'AD',
            u'AB',
            u'E',
            u'EA',
        )

    def has_word(self, character_set, text):
        return text in self._words

class TestSegmentation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._dict = TestDict()
        self._frequency_table = {u'阿':100, u'比':50}

    def _test_chunking_0(self):
        # List lengtf of 0 should yield a single empty chunk list.
        self.assertEqual([[]], zl.get_chunks('', zl.TRADITIONAL, 0, self._dict, 1, 0))

    def _test_chunking_1(self):
        # One character input should yield a single list with one chunk.
        self.assertEqual([[u'阿']], zl.get_chunks(u'阿', zl.TRADITIONAL, 0, self._dict, 1, 1))

    def _test_chunking_1(self):
        # List length of 2. Should be ignored because there's not enough input.
        self.assertEqual(
            [[u'阿']],
            zl.get_chunks(u'阿', zl.TRADITIONAL, 0, self._dict, 1, 2)
        )

    def _test_chunking_2(self):
        self.assertEqual(
            [[u'阿',u'阿']],
            zl.get_chunks(u'阿阿', zl.TRADITIONAL, 0, self._dict, 1, 2)
        )

    def _test_chunking_3(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [[u'阿',u'阿']],
            zl.get_chunks(u'阿阿', zl.TRADITIONAL, 0, self._dict, 1, 3)
        )

    def _test_chunking_4(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [[u'阿',u'比']],
            zl.get_chunks(u'阿比', zl.TRADITIONAL, 0, self._dict, 1, 3)
        )

    def _test_chunking_5(self):
        # List length of 3. Should be ignored because not enough input.
        # Max key length of 2
        self.assertEqual(
            [[u'阿',u'比'],[u'阿比']],
            zl.get_chunks(u'阿比', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_6(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [[u'阿',u'西西']],
            zl.get_chunks(u'阿西西', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_7(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [[u'阿',u'西西', u'比']],
            zl.get_chunks(u'阿西西比', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_8(self):
        self.assertEqual(
            [[u'阿',u'阿地']],
            zl.get_chunks(u'阿阿地', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_9(self):
        self.assertEqual(
            [[u'阿',u'比'], [u'阿比']],
            zl.get_chunks(u'阿比', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_10(self):
        # Requires a list of length 3.  However, for the second chunk list
        # the input runs out, so it has to return a short list.
        self.assertEqual(
            [[u'阿',u'一', u'阿'], [u'阿',u'一阿']],
            zl.get_chunks(u'阿一阿', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_11(self):
        # This case is different from the previous one because here
        # the required list length of 3 cannot be met because the input
        # does not match rather than the input running out. In this case,
        # there is only one possible chunk list.
        #self.assertTrue(False)
        self.assertEqual(
            [[u'阿',u'一', u'阿']],
            zl.get_chunks(u'阿一阿XXX', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_12(self):
        # Test when the start of the input has no matching words.
        self.assertEqual(
            [],
            zl.get_chunks('X', zl.TRADITIONAL, 0, self._dict, 1, 1)
        )

    def _test_chunking_13(self):
        self.assertEqual(
            [ [u'阿',u'比',u'一'],
              [u'阿',u'比',u'一阿'],
              [u'阿比',u'一',u'阿'],
              [u'阿比',u'一阿',u'阿'],
              [u'阿比',u'一阿', u'阿地'] ],
            zl.get_chunks(u'阿比一阿阿地', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_14(self):
        self.assertEqual(
            [ [u'一',u'阿',u'阿'],
              [u'一',u'阿',u'阿地'],
              [u'一阿',u'阿地'] ],
            zl.get_chunks(u'一阿阿地', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunking_15(self):
        self.assertEqual(
            [ [u'阿地'] ],
            zl.get_chunks(u'阿地', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def test_chunking_16(self):
        self.assertEqual(
            [ [u'阿地'] ],
            zl.get_chunks(u'阿地', zl.TRADITIONAL, 0, self._dict, 2, 3)
        )

    def _test_chunk_length(self):
        self.assertEqual(0, zl.chunk_length([]))
        self.assertEqual(3, zl.chunk_length([u'阿阿', u'比']))
        self.assertEqual(6, zl.chunk_length([u'阿阿', u'比', 'CCC']))

    def _test_split_into_contiguous_1(self):
        self.assertEqual(
            [u'你好',u'外國'],
            zl.split_into_contiguous(u'你好 外國')
        )
        self.assertEqual(
            [u'你好',u'外國'],
            zl.split_into_contiguous(u'你好。。外國')
        )
        self.assertEqual(
            [u'你好',u'外國'],
            zl.split_into_contiguous(u'你好。。外國    ')
        )

    def _test_split_into_contiguous_2(self):
        self.assertEqual(
            [u'所謂布施者', u'必獲其利益'],
            zl.split_into_contiguous(u'所謂布施者，必獲其利益，')
        )

    def test_split_into_contiguous_3(self):
        # Ignore non-Chinese characters at the start and in the middle
        # of the string.
        self.assertEqual(
            [u'所謂布施者', u'必獲其利益'],
            zl.split_into_contiguous(u'1. 所謂布施者 2. 必獲其利益，')
        )

    def _test_segmentation_1(self):
        self.assertEqual(
            [u'阿'],
            zl.segment(u'阿', zl.TRADITIONAL, self._dict, 2)
        )

    def _test_segmentation_2(self):
        self.assertEqual(
            [u'阿比', u'一阿', u'阿地'],
            zl.segment(u'阿比一阿阿地', zl.TRADITIONAL, self._dict, 2)
        )

    def _test_segmentation_3(self):
        self.assertEqual(
            [u'阿比', u'一啊', '阿地', u'阿比', u'一啊', '阿地'],
            zl.segment(u'阿比一阿阿地阿比一阿阿地', zl.TRADITIONAL, self._dict, 2)
        )

    def _test_segmentation_3(self):
        # Fail because can't match some of it
        with self.assertRaises(zl.DecompositionError) as context_manager:
            zl.segment(u'阿比阿比XX', zl.TRADITIONAL, self._dict, 2, self._frequency_table)
        error = context_manager.exception
        self.assertEqual(u'阿比阿比XX', error.text)

    def _test_segmentation_4(self):
        self.assertEqual(
            zl.segment(u'阿比一阿阿地。阿比一阿阿地', zl.TRADITIONAL, self._dict, 2)
        )

    def _test_segmentation_5(self):
        self.assertEqual(
            [u'門口',u'水果'],
            zl.segment(u'門口水果', zl.TRADITIONAL)
        )

if __name__ == '__main__':
    unittest.main()
