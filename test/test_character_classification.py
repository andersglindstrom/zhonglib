# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestCharacterClassification(unittest.TestCase):

    def test_is_unicode_kangxi_radical(self):
        self.assertTrue(zl.is_unicode_kangxi_radical(u'⼀'))
        self.assertTrue(zl.is_unicode_kangxi_radical(u'⿕'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_kangxi_radical(u'一'))

        # This is a supplemental radical not a Kangxi radical.
        self.assertFalse(zl.is_unicode_kangxi_radical(u'⺀'))

    def test_is_unicode_supplemental_radical(self):
        self.assertTrue(zl.is_unicode_supplemental_radical(u'⺀'))
        self.assertTrue(zl.is_unicode_supplemental_radical(u'⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_supplemental_radical(u'一'))

        # This is a Kangxi radical, not a supplemental radical
        self.assertFalse(zl.is_unicode_supplemental_radical(u'⿕'))

    def test_is_unicode_radical(self):
        self.assertTrue(zl.is_unicode_radical(u'⼀'))
        self.assertTrue(zl.is_unicode_radical(u'⿕'))

        self.assertTrue(zl.is_unicode_radical(u'⺀'))
        self.assertTrue(zl.is_unicode_radical(u'⻳'))

        # This is the character 'yi' and not radical number 1.
        self.assertFalse(zl.is_unicode_radical(u'一'))

    def test_is_unicode_stroke(self):
        self.assertTrue(zl.is_unicode_stroke(u'㇀'))
        self.assertTrue(zl.is_unicode_stroke(u'㇣'))

if __name__ == '__main__':
    unittest.main()
