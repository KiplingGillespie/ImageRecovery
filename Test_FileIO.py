#! python

import FileIO

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap

import os
import atexit

def getThisDirectory():
	return os.path.dirname( os.path.realpath( __file__ ) )

def getTemporaryFilename( base='temp', ext='txt' ):
	# counter variable for creating unique filenames
	if not 'count' in getTemporaryFilename.__dict__:
		getTemporaryFilename.count = 1
	else:
		getTemporaryFilename.count += 1
	
	# Modifiable 'template' of filename (in case of naming conflicts)
	template = base + '{}' + ('.' + ext if ext else '')
	split = template.split('.')
	template = split[0] + '.' + split[-1] if '.' in template else split[0]
	filename = template.format( getTemporaryFilename.count )
	
	# While a file already exists with that filename
	while os.path.exists( filename ):
		# Try a different filename
		getTemporaryFilename.count += 1
		filename = template.format( getTemporaryFilename.count )
	
	# Gets the absolute (full) path to the file
	filename = os.path.abspath( filename )
	
	# Delete the file when the program terminates, if it exists
	atexit.register( lambda f: os.remove(f) if os.path.exists(f) else None, filename )
	
	return filename


def testText():

	filename = getTemporaryFilename()
	fake_filename = getTemporaryFilename()
	assert filename != fake_filename
	assert not os.path.exists( filename ) and not os.path.exists( fake_filename )
	
	output = \
'''Hello World!
	Testing...
		Testing...
			Testing...
				Done!'''
	
	
	
	### General Case
	
	# Write text to temp file (should return True if successful)
	assert FileIO.writeText( filename, output )
	
	# The file should exist now
	assert os.path.exists( filename )
	
	# Read the text back from the file
	input = FileIO.readText( filename )
	
	# Verify that the text read matches what was written
	assert input == output

	
	
	### Edge Cases

	# Try to read text from non-existent file
	fake_input = FileIO.readText( fake_filename )
	
	# Verify that nothing was read
	assert fake_input is None


	
	### Success!
	
	return True



	
class ImageDisplay( QWidget ):

	def __init__( self, image ):
	
		super().__init__()
		
		image = image.scaledToWidth( min( image.width(), 800 ) )
		
		self.initUI( QPixmap.fromImage( image ) )
	
	def initUI( self, pixmap ):
	
		self.label = QLabel( self )
		self.label.setPixmap( pixmap )
		
		self.setGeometry( 0, 0, 500, 500 )
		self.resize( pixmap.width(), pixmap.height() )
		self.setWindowTitle( "Image Display" )
		self.show()


def testImages():

	filename = getTemporaryFilename( ext='png' )
	
	image = FileIO.readImage( getThisDirectory() + '\\' + 'peppers.jpg' )
	assert image is not None
	
	FileIO.writeImage( filename, image )
	image_copy = FileIO.readImage( filename )
	
	assert image == image_copy
	
	"""
	app = QApplication( sys.argv )
	display = ImageDisplay( image )
	sys.exit( app.exec_() )
	"""
	
	return True



if __name__ == '__main__':

	if testText() and testImages():
		print( "[Success]" )
