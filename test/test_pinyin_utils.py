# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

class TestPinyinUtils(unittest.TestCase):

    def test_parse_numbered_pinyin_1(self):
        pinyin_tuples = zl.parse_cedict_pinyin(u'[tang1]')
        self.assertEqual((u'tang', 1), pinyin_tuples[0])

    def test_parse_numbered_pinyin_2(self):
        pinyin_tuples = zl.parse_cedict_pinyin(u'[hen3 hao4]')
        self.assertEqual((u'hen', 3), pinyin_tuples[0])
        self.assertEqual((u'hao', 4), pinyin_tuples[1])

    def test_parse_numbered_pinyin_3(self):
        pinyin_tuples = zl.parse_cedict_pinyin(u'[hen1 hao5]')
        self.assertEqual((u'hen', 1), pinyin_tuples[0])
        self.assertEqual((u'hao', 0), pinyin_tuples[1])

    def test_parse_numbered_pinyin_4(self):
        pinyin_tuples = zl.parse_cedict_pinyin(u'[lu:3 guan3]')
        self.assertEqual((u'lü', 3), pinyin_tuples[0])
        self.assertEqual((u'guan', 3), pinyin_tuples[1])

    def test_parse_numbered_pinyin_5(self):
        pinyin_tuples = zl.parse_cedict_pinyin(u'[lU:3 guan3]')
        self.assertEqual((u'lÜ', 3), pinyin_tuples[0])
        self.assertEqual((u'guan', 3), pinyin_tuples[1])

    def test_format_pinyin_1(self):
        self.assertEqual(u'a', zl.format_pinyin(u'a', 0))
        self.assertEqual(u'ā', zl.format_pinyin(u'a', 1))
        self.assertEqual(u'á', zl.format_pinyin(u'a', 2))
        self.assertEqual(u'ǎ', zl.format_pinyin(u'a', 3))
        self.assertEqual(u'à', zl.format_pinyin(u'a', 4))

    def test_format_pinyin_2(self):
        self.assertEqual(u'e', zl.format_pinyin(u'e', 0))
        self.assertEqual(u'ē', zl.format_pinyin(u'e', 1))
        self.assertEqual(u'é', zl.format_pinyin(u'e', 2))
        self.assertEqual(u'ě', zl.format_pinyin(u'e', 3))
        self.assertEqual(u'è', zl.format_pinyin(u'e', 4))

    def test_format_pinyin_3(self):
        self.assertEqual(u'i', zl.format_pinyin(u'i', 0))
        self.assertEqual(u'ī', zl.format_pinyin(u'i', 1))
        self.assertEqual(u'í', zl.format_pinyin(u'i', 2))
        self.assertEqual(u'ǐ', zl.format_pinyin(u'i', 3))
        self.assertEqual(u'ì', zl.format_pinyin(u'i', 4))

    def test_format_pinyin_4(self):
        self.assertEqual(u'o', zl.format_pinyin(u'o', 0))
        self.assertEqual(u'ō', zl.format_pinyin(u'o', 1))
        self.assertEqual(u'ó', zl.format_pinyin(u'o', 2))
        self.assertEqual(u'ǒ', zl.format_pinyin(u'o', 3))
        self.assertEqual(u'ò', zl.format_pinyin(u'o', 4))

    def test_format_pinyin_5(self):
        self.assertEqual(u'u', zl.format_pinyin(u'u', 0))
        self.assertEqual(u'ū', zl.format_pinyin(u'u', 1))
        self.assertEqual(u'ú', zl.format_pinyin(u'u', 2))
        self.assertEqual(u'ǔ', zl.format_pinyin(u'u', 3))
        self.assertEqual(u'ù', zl.format_pinyin(u'u', 4))

    def test_format_pinyin_6(self):
        self.assertEqual(u'ü', zl.format_pinyin(u'ü', 0))
        self.assertEqual(u'ǖ', zl.format_pinyin(u'ü', 1))
        self.assertEqual(u'ǘ', zl.format_pinyin(u'ü', 2))
        self.assertEqual(u'ǚ', zl.format_pinyin(u'ü', 3))
        self.assertEqual(u'ǜ', zl.format_pinyin(u'ü', 4))

    def test_format_pinyin_7(self):
        self.assertEqual(u'bü', zl.format_pinyin(u'bü', 0))
        self.assertEqual(u'bǖ', zl.format_pinyin(u'bü', 1))
        self.assertEqual(u'bǘ', zl.format_pinyin(u'bü', 2))
        self.assertEqual(u'bǚ', zl.format_pinyin(u'bü', 3))
        self.assertEqual(u'bǜ', zl.format_pinyin(u'bü', 4))

    def test_format_pinyin_8(self):
        self.assertEqual(u'Shü', zl.format_pinyin(u'Shü', 0))
        self.assertEqual(u'Shǖ', zl.format_pinyin(u'Shü', 1))
        self.assertEqual(u'Shǘ', zl.format_pinyin(u'Shü', 2))
        self.assertEqual(u'Shǚ', zl.format_pinyin(u'Shü', 3))
        self.assertEqual(u'Shǜ', zl.format_pinyin(u'Shü', 4))

    def test_format_pinyin_8(self):
        self.assertEqual(u'shü', zl.format_pinyin(u'shü', 0))
        self.assertEqual(u'shǖ', zl.format_pinyin(u'shü', 1))
        self.assertEqual(u'shǘ', zl.format_pinyin(u'shü', 2))
        self.assertEqual(u'shǚ', zl.format_pinyin(u'shü', 3))
        self.assertEqual(u'shǜ', zl.format_pinyin(u'shü', 4))

    def test_format_pinyin_9(self):
        self.assertEqual(u'ai', zl.format_pinyin(u'ai', 0))
        self.assertEqual(u'āi', zl.format_pinyin(u'ai', 1))
        self.assertEqual(u'ái', zl.format_pinyin(u'ai', 2))
        self.assertEqual(u'ǎi', zl.format_pinyin(u'ai', 3))
        self.assertEqual(u'ài', zl.format_pinyin(u'ai', 4))

    def test_format_pinyin_10(self):
        self.assertEqual(u'bai', zl.format_pinyin(u'bai', 0))
        self.assertEqual(u'bāi', zl.format_pinyin(u'bai', 1))
        self.assertEqual(u'bái', zl.format_pinyin(u'bai', 2))
        self.assertEqual(u'bǎi', zl.format_pinyin(u'bai', 3))
        self.assertEqual(u'bài', zl.format_pinyin(u'bai', 4))

    def test_format_pinyin_11(self):
        self.assertEqual(u'bao', zl.format_pinyin(u'bao', 0))
        self.assertEqual(u'bāo', zl.format_pinyin(u'bao', 1))
        self.assertEqual(u'báo', zl.format_pinyin(u'bao', 2))
        self.assertEqual(u'bǎo', zl.format_pinyin(u'bao', 3))
        self.assertEqual(u'bào', zl.format_pinyin(u'bao', 4))

    def test_format_pinyin_11(self):
        self.assertEqual(u'huI', zl.format_pinyin(u'huI', 0))
        self.assertEqual(u'huĪ', zl.format_pinyin(u'huI', 1))
        self.assertEqual(u'huÍ', zl.format_pinyin(u'huI', 2))
        self.assertEqual(u'huǏ', zl.format_pinyin(u'huI', 3))
        self.assertEqual(u'huÌ', zl.format_pinyin(u'huI', 4))

    def test_format_pinyin_11(self):
        self.assertEqual(u'xiu', zl.format_pinyin(u'xiu', 0))
        self.assertEqual(u'xiū', zl.format_pinyin(u'xiu', 1))
        self.assertEqual(u'xiú', zl.format_pinyin(u'xiu', 2))
        self.assertEqual(u'xiǔ', zl.format_pinyin(u'xiu', 3))
        self.assertEqual(u'xiù', zl.format_pinyin(u'xiu', 4))

    def test_format_pinyin_12(self):
        self.assertEqual(u'rOu', zl.format_pinyin(u'rOu', 0))
        self.assertEqual(u'rŌu', zl.format_pinyin(u'rOu', 1))
        self.assertEqual(u'rÓu', zl.format_pinyin(u'rOu', 2))
        self.assertEqual(u'rǑu', zl.format_pinyin(u'rOu', 3))
        self.assertEqual(u'rÒu', zl.format_pinyin(u'rOu', 4))

    def test_format_pinyin_13(self):
        self.assertEqual(u'shuai', zl.format_pinyin(u'shuai', 0))
        self.assertEqual(u'shuāi', zl.format_pinyin(u'shuai', 1))
        self.assertEqual(u'shuái', zl.format_pinyin(u'shuai', 2))
        self.assertEqual(u'shuǎi', zl.format_pinyin(u'shuai', 3))
        self.assertEqual(u'shuài', zl.format_pinyin(u'shuai', 4))

    def test_format_pinyin_list(self):
        self.assertEqual(u'rŌushuāi', zl.format_pinyin_sequence([(u'rOu', 1),(u'shuai', 1)]))
