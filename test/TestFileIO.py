# Author(s): Adam Brassfield
# Date: October 30, 2018
# File: Test.py
# Purpose: Unit tests for Image Recovery application

import unittest
import sys
sys.path.append("../")
from FileIO import *

class TestFileIO(unittest.TestCase):

	def testReadText(self):
		self.assertEqual(readText("testIO/testFileIO.txt"), "Hello, world!")

	def testWriteText(self):
		self.assertTrue(writeText("testIO/testFileIO.txt", "Hello, world!"))
