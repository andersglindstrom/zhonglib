# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterClassification(unittest.TestCase):

    def test_is_unicode_kangxi_radical(self):
        self.assertTrue(zl.is_unicode_kangxi_radical('⼀'))
        self.assertTrue(zl.is_unicode_kangxi_radical('⿕'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_kangxi_radical('一'))

        # This is a supplemental radical not a Kangxi radical.
        self.assertFalse(zl.is_unicode_kangxi_radical('⺀'))

    def test_is_unicode_supplemental_radical(self):
        self.assertTrue(zl.is_unicode_supplemental_radical('⺀'))
        self.assertTrue(zl.is_unicode_supplemental_radical('⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_supplemental_radical('一'))

        # This is a Kangxi radical, not a supplemental radical
        self.assertFalse(zl.is_unicode_supplemental_radical('⿕'))

    def test_is_unicode_radical(self):
        self.assertTrue(zl.is_unicode_radical('⼀'))
        self.assertTrue(zl.is_unicode_radical('⿕'))

        self.assertTrue(zl.is_unicode_radical('⺀'))
        self.assertTrue(zl.is_unicode_radical('⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_radical('一'))

    def test_is_unicode_stroke(self):
        self.assertTrue(zl.is_unicode_stroke('㇀'))
        self.assertTrue(zl.is_unicode_stroke('㇣'))

class TestCharacterDecomposition(unittest.TestCase):

    # These are the in-memory representations of the decomposition
    # file.

    _character_n    = ('n', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_p    = ('p', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_q    = ('q', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_r    = ('r', zl.CHARACTER, zl.COMPOSED_OF, [ _character_n, _character_p ])
    _character_s    = ('s', zl.CHARACTER, zl.COMPOSED_OF, [ _character_r, _character_q ])
    _group_1        = ('1', zl.GROUP,     zl.COMPOSED_OF, [ _character_p, _character_q ])
    _character_t    = ('t', zl.CHARACTER, zl.COMPOSED_OF, [ _group_1, _character_n ])
    _character_u    = ('u', zl.CHARACTER, zl.VARIANT_OF, _character_t )
    _group_2        = ('2', zl.GROUP,     zl.COMPOSED_OF, [ _character_t, _group_1 ])

    def setUp(self):
        decomp_data_file = os.path.join(
                                os.path.dirname(__file__),
                                'test_decomposition_data.txt')
        self._decomposer = zl.Decomposer(decomp_data_file)
        #print(self._decomposer)

    def decompose(self, ch):
        return self._decomposer.decompose(ch)

    def test_none(self):
        with self.assertRaises(RuntimeError):
            self.decompose(None)

    def test_level_zero(self):
        # Test a simple character that has no children components.
        self.assertEqual(self._character_n, self.decompose('n'))

    def test_level_one_character(self):
        self.assertEqual(self._character_r, self.decompose('r'))

    def test_level_two_character(self):
        self.assertEqual(self._character_s, self.decompose('s'))

    def test_level_one_group(self):
        self.assertEqual(self._group_1, self.decompose('1'))

    def test_character_composed_of_group(self):
        self.assertEqual(self._character_t, self.decompose('t'))

    def test_variant(self):
        self.assertEqual(self._character_u, self.decompose('u'))

    def test_group_with_group(self):
        self.assertEqual(self._group_2, self.decompose('2'))

if __name__ == '__main__':
    unittest.main()
