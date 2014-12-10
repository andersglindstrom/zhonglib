# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterDecomposition(unittest.TestCase):

    # These are the in-memory representations of the decomposition
    # file.

    @classmethod
    def setUpClass(self):
        decomp_data_file = os.path.join(
                                os.path.dirname(__file__),
                                'test_decomposition_cycle_data.txt')
        self._decomposer = zl.CharacterDecomposer(decomp_data_file)

    def test_no_cycle(self):
        self.assertFalse(zl.is_id_in_cycle(self._decomposer, 'm'))
        self.assertFalse([], zl.is_id_in_cycle(self._decomposer, 'r'))
        self.assertFalse([], zl.is_id_in_cycle(self._decomposer, '10'))
        self.assertFalse([], zl.is_id_in_cycle(self._decomposer, 'a'))

    def test_s_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 's'))

    # 'b' is a variant of 's' but is not in a cycle directly because it
    # only refers to 's'
    def test_b_not_in_cycle(self):
        self.assertFalse(zl.is_id_in_cycle(self._decomposer, 'b'))

    def test_u_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'u'))

    def test_v_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'v'))
 
    # x has a cycle below it but is not part of the cyle itself
    def test_x_not_in_cycle(self):
        self.assertFalse(zl.is_id_in_cycle(self._decomposer, 'x'))
 
    def test_y_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'y'))
 
    def test_group_20_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, '20'))
 
    def test_group_30_in_cyle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, '30'))
 
    # For is composed of groups 3 and 4 but is not in a cycle itself
    def test_group_40_not_in_cyle(self):
        self.assertFalse(zl.is_id_in_cycle(self._decomposer, '40'))
 
    def test_c_in_cycle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'c'))

    def test_d_in_cycle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'd'))

    def test_e_in_cycle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'e'))

    def test_f_in_cycle(self):
        self.assertTrue(zl.is_id_in_cycle(self._decomposer, 'f'))

    def test_decomposer_cycles(self):
        result = zl.check_decomposer_for_cycles(self._decomposer)
        self.assertEqual(10, len(result))
        result = set(result)
        self.assertTrue('"s" is in a cycle.')
        self.assertTrue('"u" is in a cycle.')
        self.assertTrue('"v" is in a cycle.')
        self.assertTrue('"y" is in a cycle.')
        self.assertTrue('Group 20 is in a cycle.')
        self.assertTrue('Group 30 is in a cycle.')
        self.assertTrue('"c" is in a cycle.')
        self.assertTrue('"d" is in a cycle.')
        self.assertTrue('"e" is in a cycle.')
        self.assertTrue('"f" is in a cycle.')

if __name__ == '__main__':
    unittest.main()
