#! python

from PyQt5.QtGui import QImage


def readText( filename ):
	'''Reads text from a file.
	Given:
		filename = a string containing the path of the file to be read from.
			the path may be absolute or relative to the current working directory.
	Returns:
		a string containing the file text,
		or None if the file could not be read.'''
	try:
		with open( filename, 'r' ) as file:
			return file.read()
	except:
		return None

def writeText( filename, text ):
	'''Writes text to a file.
	Given:
		filename = a string containing the path of the file to be written to.
			the path may be absolute or relative to the current working directory.
		text = a string to be written to the text file.
	Returns:
		True if the text was successfully written to the file,
		False otherwise.'''
	try:
		with open( filename, 'w' ) as file:
			file.write( text )
			return True
	except:
		return False

def readImage( filename, format = None ):
	'''Reads an image from a file.
	Given:
		filename = a string containing the path of the file to be read from.
			the path may be absolute or relative to the current working directory.
		format = a case-insensitive string indicating the image file format.
			If None (the default), it attempts to deduce an appropriate
			format from the file extension.
	Returns:
		a QImage containing the file image,
		or None if the file could not be read.'''
	try:
		image = QImage()
		return image if image.load( filename, format = format ) else None
	except:
		return None

def writeImage( filename, image, format = 'png', quality = -1 ):
	'''Writes an image to a file.
	Given:
		filename = a string containing the path of the file to be written to.
			the path may be absolute or relative to the currenty working directory.
		image = a QImage to be written to the file.
		format = a case-insensitive string indicating the image file format.
			Defaults to 'png'.
			If None or empty, it attempts to deduce an appropriate format from the
				file extension.
			If not None or empty, and if the filename does not have a file extension,
				it is appended to the filename as a file extension.
		quality = the quality of jpg compression if jpg format is used.
			In range [0,100].
			-1 indicates use of Qt's default value.
	Returns:
		True if the image was successfully written to the file,
		False otherwise.'''
	try:
		if '.' not in filename and format:
			filename += '.' + format
		return image.save( filename, format = format, quality = quality )
	except:
		return False