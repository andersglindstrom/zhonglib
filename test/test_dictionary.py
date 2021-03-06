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

    def gateway_1_checks(self, result):
        self.assertEqual(u'門', result.traditional)
        self.assertEqual(u'门', result.simplified)
        self.assertEqual(u'[men2]', result.pinyin)
        self.assertEqual(5, len(result.english))
        self.assertEqual(u'gate', result.english[0])
        self.assertEqual(u'door', result.english[1])
        self.assertEqual(u'gateway', result.english[2])
        self.assertEqual(u'doorway', result.english[3])
        self.assertEqual(u'opening', result.english[4])
        self.assertEqual([u'扇', u'個'], result.traditional_measure_words)
        self.assertEqual([u'扇', u'个'], result.simplified_measure_words)

    def gateway_2_checks(self, result):
        self.assertEqual(u'門口', result.traditional)
        self.assertEqual(u'门口', result.simplified)
        self.assertEqual(u'[men2 kou3]', result.pinyin)
        self.assertEqual(2, len(result.english))
        self.assertEqual(u'doorway', result.english[0])
        self.assertEqual(u'gate', result.english[1])
        self.assertEqual([u'個'], result.traditional_measure_words)
        self.assertEqual([u'个'], result.simplified_measure_words)

    def test_traditional_1(self):
        result = self._dictionary.find(u'門', zl.TRADITIONAL)
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_1_checks(result[0])

    def test_traditional_2(self):
        result = self._dictionary.find(u'門口', zl.TRADITIONAL)
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_2_checks(result[0])

    def test_simplified_1(self):
        result = self._dictionary.find(u'门', zl.SIMPLIFIED)
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_1_checks(result[0])

    def test_simplified_2(self):
        result = self._dictionary.find(u'门口', zl.SIMPLIFIED)
        self.assertTrue(result != None)
        self.assertEqual(1, len(result))
        self.gateway_2_checks(result[0])
        
        # Lookup by english 'door'.  Should find
        # two entries.
    def test_english_1_1(self):
        result = self._dictionary.find(u'gate', include_english=True)
        self.assertTrue(result != None)
        self.assertEqual(2, len(result))
        self.gateway_2_checks(result[0])
        self.gateway_1_checks(result[1])
        
        # Lookup by english 'doorway'.  Should find
        # two entries.
    def test_english_1_2(self):
        result = self._dictionary.find(u'doorway', include_english=True)
        self.assertTrue(result != None)
        self.assertEqual(2, len(result))
        self.gateway_2_checks(result[0])
        self.gateway_1_checks(result[1])

    def test_multiple_measure_words(self):
        result = self._dictionary.find(u'課', character_set = zl.TRADITIONAL | zl.SIMPLIFIED)
        self.assertEqual(1, len(result))
        self.assertEquals([u'門',u'堂',u'節'], result[0].traditional_measure_words)
        self.assertEquals([u'门',u'堂',u'节'], result[0].simplified_measure_words)

    def test_contains(self):
        self.assertTrue(self._dictionary.has_word(zl.TRADITIONAL, u'門'))
        self.assertFalse(self._dictionary.has_word(zl.SIMPLIFIED, u'門'))
        self.assertTrue(self._dictionary.has_word(zl.TRADITIONAL | zl.SIMPLIFIED, u'門'))

        self.assertFalse(self._dictionary.has_word(zl.TRADITIONAL, u'门'))
        self.assertTrue(self._dictionary.has_word(zl.SIMPLIFIED, u'门'))
        self.assertTrue(self._dictionary.has_word(zl.TRADITIONAL | zl.SIMPLIFIED, u'门'))

        self.assertTrue(self._dictionary.has_word(zl.TRADITIONAL, u'門口'))
        self.assertFalse(self._dictionary.has_word(zl.TRADITIONAL, u'门口'))

        self.assertFalse(self._dictionary.has_word(zl.SIMPLIFIED, u'門口'))
        self.assertFalse(self._dictionary.has_word(zl.TRADITIONAL, u'门口'))

        self.assertFalse(self._dictionary.has_word(zl.TRADITIONAL, u'Hello'))

if __name__ == '__main__':
    unittest.main()
