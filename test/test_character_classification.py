# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterClassification(unittest.TestCase):

    def test_is_kangxi_radical(self):
        self.assertTrue(zl.is_kangxi_radical(u'⼀'))
        self.assertTrue(zl.is_kangxi_radical(u'⿕'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_kangxi_radical(u'一'))

        # This is a supplemental radical not a Kangxi radical.
        self.assertFalse(zl.is_kangxi_radical(u'⺀'))

        # This is the first character before the block
        self.assertFalse(zl.is_kangxi_radical(unichr(0x2EFF)))

        # This is the first character after the block
        self.assertFalse(zl.is_kangxi_radical(unichr(0x2FE0)))

    def test_is_supplemental_radical(self):
        self.assertTrue(zl.is_supplemental_radical(u'⺀'))
        self.assertTrue(zl.is_supplemental_radical(u'⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_supplemental_radical(u'一'))

        # This is a Kangxi radical, not a supplemental radical
        self.assertFalse(zl.is_supplemental_radical(u'⿕'))

        # This is the first character before the block
        self.assertFalse(zl.is_supplemental_radical(unichr(0x2E7F)))

        # This is the first character after the block
        self.assertFalse(zl.is_supplemental_radical(unichr(0x2F00)))

    def test_is_radical(self):
        self.assertTrue(zl.is_radical(u'⼀'))
        self.assertTrue(zl.is_radical(u'⿕'))

        self.assertTrue(zl.is_radical(u'⺀'))
        self.assertTrue(zl.is_radical(u'⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_radical(u'一'))

    def test_is_stroke(self):
        self.assertTrue(zl.is_stroke(u'㇀'))
        self.assertTrue(zl.is_stroke(u'㇣'))

        # This is the first character before the block
        self.assertFalse(zl.is_kangxi_radical(unichr(0x31C0)))

        # This is the first character after the block
        self.assertFalse(zl.is_kangxi_radical(unichr(0x31E3)))

    def test_is_unified_character(self):
        pass

if __name__ == '__main__':
    unittest.main()
