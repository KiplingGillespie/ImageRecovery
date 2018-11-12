# Author(s): Adam Brassfield
# Date: November 6, 2018
# File: TestCommentCounter.py

import unittest # Python's native testing library
import sys
sys.path.append("../") # Used to access modules in parent directory
from FileIO import * # Needed to use CommentCounter
from CommentCounter import * # Module being tested

# Testing class for functions in CommentCounter.py (located in parent directory)
class TestCommentCounter(unittest.TestCase):
	# Tests the function 'getComments' in CommentCounter.py
	# Uses a text file for input located in the directory 'testIO'
	def testGetComments(self):
		text = FileIO.readText("test/testIO/testCommentCounter.txt")
		self.assertEqual(getComments(text), ["This is a comment"]) 

	# Tests the function 'getWords' in CommentCounter.py
	# Uses a text file for input located in the directory 'testIO'
	def testGetWords(self):
		text = FileIO.readText("test/testIO/testCommentCounter.txt")
		self.assertEqual(getWords(text), ["This", "is", "a", "comment", "But", "I", "am", "not"])

if __name__=='__main__':
	unittest.main()
