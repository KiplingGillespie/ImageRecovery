# Author(s): Adam Brassfield
# Date: November 6, 2018
# File: TestCommentCounter.py

import unittest
import sys
sys.path.append("../")
from FileIO import *
from CommentCounter import *

class TestCommentCounter(unittest.TestCase):
	def testGetComments(self):
		text = FileIO.readText("test/testIO/testCommentCounter.txt")
		self.assertEquals(getComments(text), ["This is a comment"]) 

	def testGetWords(self):
		text = FileIO.readText("test/testIO/testCommentCounter.txt")
		self.assertEquals(getWords(text), ["This", "is", "a", "comment", "But", "I", "am", "not"])
