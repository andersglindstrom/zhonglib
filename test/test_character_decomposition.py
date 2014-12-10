# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterDecomposition(unittest.TestCase):

    # These are the in-memory representations of the decomposition
    # file.

    _character_m    = ('m', zl.CHARACTER, zl.COMPOSED_OF, None, 1)
    _character_n    = ('n', zl.CHARACTER, zl.COMPOSED_OF, None, 2)
    _character_p    = ('p', zl.CHARACTER, zl.COMPOSED_OF, None, 3)
    _character_q    = ('q', zl.CHARACTER, zl.COMPOSED_OF, None, 4)
    _character_r    = ('r', zl.CHARACTER, zl.COMPOSED_OF, [ _character_m, _character_n, _character_p ], 5)
    _character_s    = ('s', zl.CHARACTER, zl.COMPOSED_OF, [ _character_r, _character_q ], 6)
    _group_1        = ('1', zl.GROUP,     zl.COMPOSED_OF, [ _character_p, _character_q ], 7)
    _character_t    = ('t', zl.CHARACTER, zl.COMPOSED_OF, [ _group_1, _character_n ], 8)
    _character_u    = ('u', zl.CHARACTER, zl.VARIANT_OF, _character_t, 9 )
    _group_2        = ('2', zl.GROUP,     zl.COMPOSED_OF, [ _character_t, _group_1 ], 10)
    _character_zi   = (u'子', zl.CHARACTER, zl.COMPOSED_OF, None, 11)
    _character_nu   = (u'女', zl.CHARACTER, zl.COMPOSED_OF, None, 12)
    _character_hao  = (u'好', zl.CHARACTER, zl.COMPOSED_OF, [_character_nu, _character_zi], 13)

    @classmethod
    def setUpClass(self):
        decomp_data_file = os.path.join(
                                os.path.dirname(__file__),
                                'test_decomposition_data.txt')
        self._decomposer = zl.CharacterDecomposer(decomp_data_file)

    def decomposition_tree(self, ch):
        return self._decomposer.decomposition_tree(ch)

    def test_none(self):
        with self.assertRaises(zl.ZhonglibException) as cm:
            self.decomposition_tree(u'行')
        exception = cm.exception
        self.assertEqual(u'No decomposition data for "行"', exception.message)

    def test_level_zero(self):
        # Test a simple character that has no children components.
        self.assertEqual(self._character_n, self.decomposition_tree('n'))

    def test_level_one_character(self):
        self.assertEqual(self._character_r, self.decomposition_tree('r'))

    def test_level_two_character(self):
        self.assertEqual(self._character_s, self.decomposition_tree('s'))

    def test_level_one_group(self):
        self.assertEqual(self._group_1, self.decomposition_tree('1'))

    def test_character_composed_of_group(self):
        self.assertEqual(self._character_t, self.decomposition_tree('t'))

    def test_variant(self):
        self.assertEqual(self._character_u, self.decomposition_tree('u'))

    def test_group_with_group(self):
        self.assertEqual(self._group_2, self.decomposition_tree('2'))

    def test_utf8(self):
        self.assertEqual(self._character_zi, self.decomposition_tree(u'子'))
        self.assertEqual(self._character_nu, self.decomposition_tree(u'女'))
        self.assertEqual(self._character_hao, self.decomposition_tree(u'好'))

    def test_flatten_decomposition(self):
        self.assertEquals([], zl.flatten_decomposition(self._character_m))
        self.assertEquals(['m', 'n', 'p'], zl.flatten_decomposition(self._character_r))
        self.assertEquals(['p', 'q'], zl.flatten_decomposition(self._group_1))
        self.assertEquals(['p', 'q', 'n'], zl.flatten_decomposition(self._character_t))
        self.assertEquals(['t'], zl.flatten_decomposition(self._character_u))
        self.assertEquals(['t', 'p', 'q'], zl.flatten_decomposition(self._group_2))

    def test_contains(self):
        self.assertTrue('m' in self._decomposer)
        self.assertTrue(u'好' in self._decomposer)
        self.assertFalse('z' in self._decomposer)

    def test_getitem(self):
        self.assertEquals(self._character_m, self._decomposer['m'])
        self.assertEquals(self._character_n, self._decomposer['n'])

    def test_standard_decomposer_1(self):
        decomposition = zl.decompose_character(u'好', flatten=True)
        self.assertEquals([u'女', u'子'], decomposition)

    def test_standard_decomposer_2(self):
        decomposition = zl.decompose_character(u'乜', flatten=True)
        self.assertEquals([u'㇟', u'㇆'], decomposition)

if __name__ == '__main__':
    unittest.main()
