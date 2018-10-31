# Author(s): Adam Brassfield
# Date: October 30, 2018
# File: Test.py
# Purpose: Unit tests for Image Recovery application

from FileIO import *
import unittest

class TestIO(unittest.TestCase):

	def testReadText(self):
		self.assertEqual(readText("test/testTextFile.txt"), "Hello, world!\n")

