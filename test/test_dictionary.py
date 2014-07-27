# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import zhonglib as zl

class TestDictionary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dictionary_file = os.path.join(
                os.path.dirname(__file__),
                'test_dictionary.txt')
        dictionary_dir = os.path.join(
                os.path.dirname(__file__),
                'test_dictionary')
        if os.path.exists(dictionary_dir):
            shutil.rmtree(dictionary_dir)
        zl.create_dictionary(dictionary_file, dictionary_dir)
        self._dictionary = zl.Dictionary(dictionary_dir)

    def gateway_checks(self, result):
        self.assertEqual(u'门口', result.simplified)
        self.assertEqual(u'門口', result.traditional)
        self.assertEqual(u'[men2 kou3]', result.pinyin)
        self.assertEqual(u'/doorway/gate/CL:個|个[ge4]/', result.raw_meaning)

    def test_traditional_1(self):
        result = self._dictionary.find(u'門口')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_checks(result[0])

    def test_simplified_1(self):
        result = self._dictionary.find(u'门口')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_checks(result[0])
        
    def test_meaning_1_1(self):
        result = self._dictionary.find(u'gate')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_checks(result[0])
        
    def test_meaning_1_2(self):
        result = self._dictionary.find(u'doorway')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_checks(result[0])

if __name__ == '__main__':
    unittest.main()
