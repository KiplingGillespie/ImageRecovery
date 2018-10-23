#! python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import	(QApplication, QMainWindow, QAction,
	QFileDialog,
	QLabel, QScrollArea)
from PyQt5.QtGui import QIcon, QPixmap, QImage

import os
os.chdir( os.path.dirname( os.path.realpath( __file__ ) ) )

import FileIO


class ImageRestorationApp( QMainWindow ):

	def __init__( self ):

		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
		
		# Creates a label to display an image
		self.image_label = QLabel( self )
		self.image_label.setText( "Open an image to begin (File -> Open)" )
		
		# Creates a scroll area for large images
		self.image_scrolly = QScrollArea( self )
		self.image_scrolly.setWidget( self.image_label )
		self.image_scrolly.setWidgetResizable( True )
		
		# Centers the scroll area
		self.setCentralWidget( self.image_scrolly )
		
		# Initializes all QActions used by the application
		self.initActions()
		
		# Adds a status bar to the bottom of the application window
		self.statusBar()
		
		# Adds a menu bar at the top of the application window
		menubar = self.menuBar()

		# Populates the menu bar with various menus and actions
		file_menu = menubar.addMenu( '&File' )
		file_menu.addAction( self.open_act )
		file_menu.addAction( self.exit_act )
		restore_menu = menubar.addMenu( '&Restoration' )
		restore_menu.addAction( self.restore_act )
		
		# Adds a (movable) tool bar just below the menu bar
		toolbar = self.addToolBar( 'Toolbar' )
		
		# Adds some frequently used actions to the tool bar
		toolbar.addAction( self.restore_act )
		
		# X-Pos, Y-Pos, Width, Height
		self.setGeometry( 200, 200, 500, 500 )
		self.setWindowTitle( 'Image Restoration' )
		
		self.show()
	

	def initAction( self, label, trigger, shortcut = None, status = None, icon = QIcon('') ):
		'''Creates a QAction object with the provided parameters.
		Given:
			label = a string containing a text name/label for the action.
			trigger = a callable object (i.e. function) to be called
				when the action is triggered.
			shortcut = a string representing a keyboard shortcut to trigger the action.
				Defaults to None.
			status = a string containing a message to display on the statusbar
				when the action is hovered over with the mouse.
				Defaults to None.
			icon = a QIcon to be displayed next to the action's name/label
				Defaults to a blank QIcon.
		Returns:
			A QAction object as described by the passed parameters.'''
		
		act = QAction( icon, label, self )
		if shortcut:
			act.setShortcut( shortcut )
		if status:
			act.setStatusTip( status )
		act.triggered.connect( trigger )
		return act

	def initActions( self ):
		'''Initializes each action used by the application.'''

		self.open_act = self.initAction( 'Open', self.openImage, shortcut='Ctrl+O', status='Open Image' )
		self.exit_act = self.initAction( 'Exit', self.close, shortcut='Alt+F4', status='Exit Application' )
		self.restore_act = self.initAction( 'Restore', self.restoreImage, shortcut='Ctrl+Enter', status='Restore Image' )
	
	
	def openImage( self ):
		'''Prompts the user to select an image file and loads it into the application.'''
	
		filename = QFileDialog.getOpenFileName(	self, 'Open File',
			os.getcwd(),
			'Images (*.png *.jpg)' )
		
		self.image = FileIO.readImage( filename[0] )
		self.image_label.setPixmap( QPixmap( self.image ) )
	
	def restoreImage( self ):
		'''Passes the current image through the restoration model, displaying the resulting restored image'''
		
		pass
		
		# output = model.toImage( model.input( model.toNdArray( self.image ) ) )
		# (or something)


	
if __name__ == '__main__':

	app = QApplication( sys.argv )

	# Instantiates the application window
	image_restoration_app = ImageRestorationApp()

	sys.exit( app.exec_() )