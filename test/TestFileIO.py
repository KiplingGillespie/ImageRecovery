# Author(s): Adam Brassfield
# Date: October 30, 2018
# File: Test.py

import unittest # Python's native testing library 
import sys
sys.path.append("../") # Used to access module in parent directory
from FileIO import * # Module being test

class TestFileIO(unittest.TestCase):
	# Tests the function 'readText' using text file in 'testIO' directory
	def testReadText(self):
		self.assertEqual(readText("testIO/testFileIO.txt"), "Hello, world!")
	# Test the function 'writeText' using text file in 'testIO' directory
	def testWriteText(self):
		self.assertTrue(writeText("testIO/testFileIO.txt", "Hello, world!"))

if __name__=='__main__':
	unittest.main()
