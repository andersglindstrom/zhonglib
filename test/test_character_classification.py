# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterClassification(unittest.TestCase):

    def test_is_unified_character(self):
        self.assertFalse(zl.is_unified_character(unichr(0x4E00-1)))
        self.assertTrue(zl.is_unified_character(unichr(0x4E00)))
        self.assertTrue(zl.is_unified_character(unichr(0x9FFF)))
        self.assertFalse(zl.is_unified_character(unichr(0x9FFF+1)))

    def test_is_unified_extension_A_character(self):
        self.assertFalse(zl.is_unified_extension_A_character(unichr(0x3400-1)))
        self.assertTrue(zl.is_unified_extension_A_character(unichr(0x3400)))
        self.assertTrue(zl.is_unified_extension_A_character(unichr(0x4DBF)))
        self.assertFalse(zl.is_unified_extension_A_character(unichr(0x4DBF+1)))

    def test_is_unified_extension_B_character(self):
        self.assertFalse(zl.is_unified_extension_B_character(unichr(0x20000-1)))
        self.assertTrue(zl.is_unified_extension_B_character(unichr(0x20000)))
        self.assertTrue(zl.is_unified_extension_B_character(unichr(0x2A6DF)))
        self.assertFalse(zl.is_unified_extension_B_character(unichr(0x2A6DF+1)))

    def test_is_unified_extension_C_character(self):
        self.assertFalse(zl.is_unified_extension_C_character(unichr(0x2A700-1)))
        self.assertTrue(zl.is_unified_extension_C_character(unichr(0x2A700)))
        self.assertTrue(zl.is_unified_extension_C_character(unichr(0x2B73F)))
        self.assertFalse(zl.is_unified_extension_C_character(unichr(0x2B73F+1)))

    def test_is_unified_extension_D_character(self):
        self.assertFalse(zl.is_unified_extension_D_character(unichr(0x2B740-1)))
        self.assertTrue(zl.is_unified_extension_D_character(unichr(0x2B740)))
        self.assertTrue(zl.is_unified_extension_D_character(unichr(0x2B81F)))
        self.assertFalse(zl.is_unified_extension_D_character(unichr(0x2B81F+1)))

    def test_is_supplemental_radical(self):
        self.assertFalse(zl.is_supplemental_radical(unichr(0x2E80-1)))
        self.assertTrue(zl.is_supplemental_radical(unichr(0x2E80)))
        self.assertTrue(zl.is_supplemental_radical(unichr(0x2EFF)))
        self.assertFalse(zl.is_supplemental_radical(unichr(0x2EFF+1)))

    def test_is_kangxi_radical(self):
        self.assertFalse(zl.is_kangxi_radical(unichr(0x2F00-1)))
        self.assertTrue(zl.is_kangxi_radical(unichr(0x2F00)))
        self.assertTrue(zl.is_kangxi_radical(unichr(0x2FDF)))
        self.assertFalse(zl.is_kangxi_radical(unichr(0x2FDF+1)))

    def test_is_description_character(self):
        self.assertFalse(zl.is_description_character(unichr(0x2FF0-1)))
        self.assertTrue(zl.is_description_character(unichr(0x2FF0)))
        self.assertTrue(zl.is_description_character(unichr(0x2FFF)))
        self.assertFalse(zl.is_description_character(unichr(0x2FFF+1)))

    def test_is_symbol_or_punctuation(self):
        self.assertFalse(zl.is_symobl_or_punctuation(unichr(0x3000-1)))
        self.assertTrue(zl.is_symobl_or_punctuation(unichr(0x3000)))
        self.assertTrue(zl.is_symobl_or_punctuation(unichr(0x303F)))
        self.assertFalse(zl.is_symobl_or_punctuation(unichr(0x303F+1)))

    def test_is_stroke(self):
        self.assertFalse(zl.is_stroke(unichr(0x31C0-1)))
        self.assertTrue(zl.is_stroke(unichr(0x31C0)))
        self.assertTrue(zl.is_stroke(unichr(0x31EF)))
        self.assertFalse(zl.is_stroke(unichr(0x31EF+1)))

    def test_is_enclosed_letter_or_month(self):
        self.assertFalse(zl.is_enclosed_letter_or_month(unichr(0x3200-1)))
        self.assertTrue(zl.is_enclosed_letter_or_month(unichr(0x3200)))
        self.assertTrue(zl.is_enclosed_letter_or_month(unichr(0x32FF)))
        self.assertFalse(zl.is_enclosed_letter_or_month(unichr(0x32FF+1)))

    def test_is_compatibility_character(self):
        self.assertFalse(zl.is_compatibility_character(unichr(0x3300-1)))
        self.assertTrue(zl.is_compatibility_character(unichr(0x3300)))
        self.assertTrue(zl.is_compatibility_character(unichr(0x33FF)))
        self.assertFalse(zl.is_compatibility_character(unichr(0x33FF+1)))

    def test_is_compatibility_ideograph(self):
        self.assertFalse(zl.is_compatibility_ideograph(unichr(0xF900-1)))
        self.assertTrue(zl.is_compatibility_ideograph(unichr(0xF900)))
        self.assertTrue(zl.is_compatibility_ideograph(unichr(0xFAFF)))
        self.assertFalse(zl.is_compatibility_ideograph(unichr(0xFAFF+1)))

    def test_is_compatibility_ideograph_supplement(self):
        self.assertFalse(zl.is_compatibility_ideograph_supplement(unichr(0x2F800-1)))
        self.assertTrue(zl.is_compatibility_ideograph_supplement(unichr(0x2F800)))
        self.assertTrue(zl.is_compatibility_ideograph_supplement(unichr(0x2FA1F)))
        self.assertFalse(zl.is_compatibility_ideograph_supplement(unichr(0x2FA1F+1)))

    def test_is_cjk_character(self):
        pass

    def test_is_radical(self):
        self.assertTrue(zl.is_radical(u'⼀'))
        self.assertTrue(zl.is_radical(u'⿕'))

        self.assertTrue(zl.is_radical(u'⺀'))
        self.assertTrue(zl.is_radical(u'⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_radical(u'一'))

if __name__ == '__main__':
    unittest.main()
