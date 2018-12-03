#! python

from PyQt5.QtWidgets import	(QWidget, QLabel, QScrollArea,
	QVBoxLayout,
	QFileDialog)
from PyQt5.QtGui import	QIcon, QImage, QPixmap
from PyQt5.QtCore import	Qt

import os

import FileIO
import QtHelper

import Clean


class RestorationWidget( QWidget ):

	def __init__( self ):
	
		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
	
		vbox	= QVBoxLayout()
	
		# Creates a label to display an image
		self.image_label = QLabel( self )
		self.image_label.setAlignment( Qt.AlignCenter )
		self.image_label.setText( "Open an image to begin (File -> Open)" )
		
		self.image_filename	= None
		
		# Creates a scroll area for large images
		self.image_scrolly = QScrollArea( self )
		self.image_scrolly.setWidget( self.image_label )
		self.image_scrolly.setWidgetResizable( True )
		
		vbox.addWidget( self.image_scrolly )
		self.setLayout( vbox )
	
	
	### Actions ###
	
	def openImage( self ):
		'''Prompts the user to select an image file and loads it into the application.'''
	
		filename = QFileDialog.getOpenFileName(	self, 'Open File',
			os.getcwd(),
			'Images (*.png *.jpg)' )
		
		read_image = FileIO.readImage( filename[0] )
		
		if read_image is None:
			pass # Error (weird)
		else:
			self.image = read_image
			self.image_filename	= filename
			self.image_label.setPixmap( QPixmap( self.image ) )
	
	def restoreImage( self ):
		'''Passes the current image through the restoration model, displaying the resulting restored image.'''
		
		if self.image_filename is None:
			QtHelper.dialog( 'Before restoring an image, please open it using File->Open (Ctrl+O)' )
			return
		
		#QtHelper.dialog( 'image restoration is not yet implemented' )
		
		input_filename	= self.image_filename
		output_filename	= 'temp_restored_image.png'
		
		Clean.Clean( input_filename[0], output_filename )
		
		read_image	= FileIO.readImage( output_filename )
		
		if read_image is None:
			pass # Error (very weird)
		else:
			self.image = read_image
			self.image_filename = output_filename
			self.image_label.setPixmap( QPixmap( self.image ) )