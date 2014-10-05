# -*- coding: utf-8 -*-

import unittest
import zhonglib as zl

class TestExceptions(unittest.TestCase):

    def test_1(self):
        ex = zl.DecompositionError(u'中山路')
        message = ""+ unicode(ex)
