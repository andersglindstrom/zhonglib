# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestSegmentation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._dict = {
            'A':None,
            'B':None,
            'CC':None,
            'AD':None,
            'AB':None,
            'E':None,
            'EA':None,
        }

    def _test_chunking_0(self):
        # List lengtf of 0 should yield a single empty chunk list.
        self.assertEqual([[]], zl.get_chunks('', 0, self._dict, 1, 0))

    def _test_chunking_1(self):
        # One character input should yield a single list with one chunk.
        self.assertEqual([['A']], zl.get_chunks('A', 0, self._dict, 1, 1))

    def _test_chunking_1(self):
        # List length of 2. Should be ignored because there's not enough input.
        self.assertEqual(
            [['A']],
            zl.get_chunks('A', 0, self._dict, 1, 2)
        )

    def _test_chunking_2(self):
        self.assertEqual(
            [['A','A']],
            zl.get_chunks('AA', 0, self._dict, 1, 2)
        )

    def _test_chunking_3(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','A']],
            zl.get_chunks('AA', 0, self._dict, 1, 3)
        )

    def _test_chunking_4(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','B']],
            zl.get_chunks('AB', 0, self._dict, 1, 3)
        )

    def _test_chunking_5(self):
        # List length of 3. Should be ignored because not enough input.
        # Max key length of 2
        self.assertEqual(
            [['A','B']],
            zl.get_chunks('AB', 0, self._dict, 2, 3)
        )

    def _test_chunking_6(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','CC']],
            zl.get_chunks('ACC', 0, self._dict, 2, 3)
        )

    def _test_chunking_7(self):
        # List length of 3. Should be ignored because not enough input.
        self.assertEqual(
            [['A','CC', 'B']],
            zl.get_chunks('ACCB', 0, self._dict, 2, 3)
        )

    def _test_chunking_8(self):
        self.assertEqual(
            [['A','AD']],
            zl.get_chunks('AAD', 0, self._dict, 2, 3)
        )

    def test_chunking_9(self):
        self.assertEqual(
            [['A','B'], ['AB']],
            zl.get_chunks('AB', 0, self._dict, 2, 3)
        )

    def test_chunking_10(self):
        # Requires a list of length 3.  However, for the second chunk list
        # the input runs out, so it has to return a short list.
        self.assertEqual(
            [['A','E', 'A'], ['A','EA']],
            zl.get_chunks('AEA', 0, self._dict, 2, 3)
        )

    def test_chunking_11(self):
        # This case is different from the previous one because here
        # the required list length of 3 cannot be met because the input
        # does not match rather than the input running out. In this case,
        # there is only one possible chunk list.
        self.assertEqual(
            [['A','E', 'A']],
            zl.get_chunks('AEAXXX', 0, self._dict, 2, 3)
        )

    def test_chunking_12(self):
        # Test when the start of the input has no matching words.
        self.assertEqual(
            [],
            zl.get_chunks('X', 0, self._dict, 1, 1)
        )

    def test_chunking_13(self):
        self.assertEqual(
            [ ['A','B','E'],
              ['A','B','EA'],
              ['AB','E','A'],
              ['AB','EA','A'],
              ['AB','EA', 'AD'] ],
            zl.get_chunks('ABEAAD', 0, self._dict, 2, 3)
        )

    def test_chunking_14(self):
        self.assertEqual(
            [ ['E','A','A'],
              ['E','A','AD'],
              ['EA','AD'] ],
            zl.get_chunks('EAAD', 0, self._dict, 2, 3)
        )

    def test_chunking_15(self):
        self.assertEqual(
            [ ['AD'] ],
            zl.get_chunks('AD', 0, self._dict, 2, 3)
        )

    def test_chunk_length(self):
        self.assertEqual(0, zl.chunk_length([]))
        self.assertEqual(3, zl.chunk_length(['AA', 'B']))
        self.assertEqual(6, zl.chunk_length(['AA', 'B', 'CCC']))

    def test_segmentation_1(self):
        self.assertEqual(
            ['A'],
            zl.segment('A', self._dict, 2)
        )

    def test_segmentation_2(self):
        self.assertEqual(
            ['AB', 'EA', 'AD'],
            zl.segment('ABEAAD', self._dict, 2)
        )
