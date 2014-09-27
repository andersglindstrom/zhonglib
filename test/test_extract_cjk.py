# -*- coding: utf-8 -*-

import os.path
import unittest
import zhonglib as zl

class TestExtractCJK(unittest.TestCase):

    def test_0(self):
        pattern, words = zl.extract_cjk('')
        self.assertEqual('', pattern)
        self.assertEqual((), words)
        self.assertEqual('', pattern%words)

    def test_1(self):
        pattern, words = zl.extract_cjk('Hello, world.')
        self.assertEqual(u'Hello, world.', pattern)
        self.assertEqual((), words)
        self.assertEqual(u'Hello, world.', pattern%words)

    def test_2(self):
        pattern, words = zl.extract_cjk(u'你好, world.')
        self.assertEqual(u'%s, world.', pattern)
        self.assertEqual((u'你好',), words)
        self.assertEqual(u'你好, world.', pattern%words)

    def test_3(self):
        pattern, words = zl.extract_cjk(u'你好, world. 門口人 to the door.')
        self.assertEqual(u'%s, world. %s to the door.', pattern)
        self.assertEqual((u'你好', u'門口人'), words)
        self.assertEqual(u'你好, world. 門口人 to the door.', pattern%words)

    def test_4(self):
        pattern, words = zl.extract_cjk(u'你好, world. 門口人')
        self.assertEqual(u'%s, world. %s', pattern)
        self.assertEqual((u'你好', u'門口人'), words)
        self.assertEqual(u'你好, world. 門口人', pattern%words)
