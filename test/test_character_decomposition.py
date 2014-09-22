# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterDecomposition(unittest.TestCase):

    # These are the in-memory representations of the decomposition
    # file.

    _character_m    = ('m', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_n    = ('n', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_p    = ('p', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_q    = ('q', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_r    = ('r', zl.CHARACTER, zl.COMPOSED_OF, [ _character_m, _character_n, _character_p ])
    _character_s    = ('s', zl.CHARACTER, zl.COMPOSED_OF, [ _character_r, _character_q ])
    _group_1        = ('1', zl.GROUP,     zl.COMPOSED_OF, [ _character_p, _character_q ])
    _character_t    = ('t', zl.CHARACTER, zl.COMPOSED_OF, [ _group_1, _character_n ])
    _character_u    = ('u', zl.CHARACTER, zl.VARIANT_OF, _character_t )
    _group_2        = ('2', zl.GROUP,     zl.COMPOSED_OF, [ _character_t, _group_1 ])
    _character_nu   = (u'女', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_zi   = (u'子', zl.CHARACTER, zl.COMPOSED_OF, None)
    _character_hao  = (u'好', zl.CHARACTER, zl.COMPOSED_OF, [_character_nu, _character_zi])

    @classmethod
    def setUpClass(self):
        decomp_data_file = os.path.join(
                                os.path.dirname(__file__),
                                'test_decomposition_data.txt')
        self._decomposer = zl.CharacterDecomposer(decomp_data_file)

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

    def test_utf8(self):
        self.assertEqual(self._character_zi, self.decompose(u'子'))
        self.assertEqual(self._character_nu, self.decompose(u'女'))
        self.assertEqual(self._character_hao, self.decompose(u'好'))

    def test_flatten_decomposition(self):
        self.assertEquals(['m'], zl.flatten_decomposition(self._character_m))
        self.assertEquals(['m', 'n', 'p'], zl.flatten_decomposition(self._character_r))
        self.assertEquals(['p', 'q'], zl.flatten_decomposition(self._group_1))
        self.assertEquals(['p', 'q', 'n'], zl.flatten_decomposition(self._character_t))
        self.assertEquals(['p', 'q', 'n'], zl.flatten_decomposition(self._character_u))
        self.assertEquals(['t', 'p', 'q'], zl.flatten_decomposition(self._group_2))

if __name__ == '__main__':
    unittest.main()
