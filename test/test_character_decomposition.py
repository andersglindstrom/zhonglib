# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

# In the following tests it is important to keep in mind
# that radical '㇐' is not the same as the character '一'.
# They have different unicode values but are usually rendered
# identically.
#
# Each character can have a 'level' assigned to it, which
# reflects how many decompositions are required to reach
# the a level 0 component.  That is, a level 0 component
# cannot be decomposed any further.
#
# It seems that the decomposition data does not use
# Unicode radicals.  Rather, the very lowest components
# are strokes.
#
# Radical are not always level 0 components because they
# can be composed of other components. However, they may
# be level 0 components.

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

    def test_none(self):
        #self.assertEqual([], zl.decompose_character(None))
        pass

    def test_radical(self):
        # Test that a simple radical is decomposed into nothing. See note
        # above.
        radical_one = '㇐'
        self.assertTrue(zl.is_unicode_stroke(radical_one))
        self.assertEqual([], zl.decompose_character(radical_one))

    def test_level_1_character(self):
        # Test that the character  '一' is decomposed into the
        # radical '㇐'.  See note above previous test.
        character_yi = '一'
        radical_one = '㇐'

        self.assertTrue(zl.is_unicode_stroke(radical_one))
        self.assertFalse(zl.is_unicode_radical(character_yi))
        self.assertEqual([radical_one], zl.decompose_character(character_yi))

    def test_level_2_character(self):
        self.assertEqual(['㇓', '㇒'], zl.decompose_character('⺁'))

if __name__ == '__main__':
    unittest.main()
