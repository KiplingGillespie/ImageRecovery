#! python

import re
import os
os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )
from functools import partial

import FileIO


def getComments( text ):
	if 're_comments' not in getComments.__dict__:
		getComments.re_comments = re.compile( r'([\'"])\1\1(.*?)\1{3}|#([^\n]*)', flags = re.DOTALL )
	return [comment[1] if comment[1] else comment[2] for comment in getComments.re_comments.findall( text )]

def getWords( text ):
	if 're_words' not in getWords.__dict__:
		getWords.re_words = re.compile( r'\b\w+' )
	return [word for word in getWords.re_words.findall( text )]


if __name__ == '__main__':
	
	prompt = partial( input, "filename to count comment words in: " )
	
	filename = prompt()
	while filename and filename not in {'quit', 'quit()', '\x1a' }:
		text = FileIO.readText( filename )
		
		print( sum( map( lambda x: len(getWords(x)), getComments( text ) ) ) )
		
		filename = prompt()