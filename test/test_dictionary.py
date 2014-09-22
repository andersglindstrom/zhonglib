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
        zl.create_dictionary(dictionary_file, dictionary_dir, True)
        self._dictionary = zl.Dictionary(dictionary_dir)

    def gateway_1_checks(self, result):
        self.assertEqual(u'門', result.traditional)
        self.assertEqual(u'门', result.simplified)
        self.assertEqual(u'[men2]', result.pinyin)
        self.assertEqual(5, len(result.meaning))
        self.assertEqual(u'gate', result.meaning[0])
        self.assertEqual(u'door', result.meaning[1])
        self.assertEqual(u'gateway', result.meaning[2])
        self.assertEqual(u'doorway', result.meaning[3])
        self.assertEqual(u'opening', result.meaning[4])
        self.assertEqual([u'扇', u'個'], result.traditional_measure_words)
        self.assertEqual([u'扇', u'个'], result.simplified_measure_words)

    def gateway_2_checks(self, result):
        self.assertEqual(u'門口', result.traditional)
        self.assertEqual(u'门口', result.simplified)
        self.assertEqual(u'[men2 kou3]', result.pinyin)
        self.assertEqual(2, len(result.meaning))
        self.assertEqual(u'doorway', result.meaning[0])
        self.assertEqual(u'gate', result.meaning[1])
        self.assertEqual([u'個'], result.traditional_measure_words)
        self.assertEqual([u'个'], result.simplified_measure_words)

    def test_traditional_1(self):
        result = self._dictionary.find(u'門')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_1_checks(result[0])

    def test_traditional_2(self):
        result = self._dictionary.find(u'門口')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_2_checks(result[0])

    def test_simplified_1(self):
        result = self._dictionary.find(u'门')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_1_checks(result[0])

    def test_simplified_2(self):
        result = self._dictionary.find(u'门口')
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_2_checks(result[0])
        
        # Lookup by meaning 'door'.  Should find
        # two entries.
    def test_meaning_1_1(self):
        result = self._dictionary.find(u'gate')
        self.assertTrue(result != None)
        self.assertEqual(2, len(result))
        self.gateway_2_checks(result[0])
        self.gateway_1_checks(result[1])
        
        # Lookup by meaning 'doorway'.  Should find
        # two entries.
    def test_meaning_1_2(self):
        result = self._dictionary.find(u'doorway')
        self.assertTrue(result != None)
        self.assertEqual(2, len(result))
        self.gateway_2_checks(result[0])
        self.gateway_1_checks(result[1])

if __name__ == '__main__':
    unittest.main()
