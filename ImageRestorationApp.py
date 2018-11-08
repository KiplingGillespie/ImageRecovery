#! python

from PyQt5.QtWidgets import	(QApplication, QMainWindow, QAction,
	QFileDialog, QMessageBox,
	QLabel, QScrollArea, QStackedWidget, QWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QStandardPaths

from ModelTrainingWidget import ModelTrainingWidget


import sys
import os
os.chdir( QStandardPaths.writableLocation( QStandardPaths.StandardLocation.DocumentsLocation ) )

import FileIO


class ImageRestorationApp( QMainWindow ):

	def __init__( self ):

		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
		
		# Enables switching between Image Restoration and Model Training GUIs
		self.stack = QStackedWidget( self )

		""" Image Restoration Mode """
		
		# Creates a label to display an image
		self.image_label = QLabel( self )
		self.image_label.setAlignment( Qt.AlignCenter )
		self.image_label.setText( "Open an image to begin (File -> Open)" )
		
		# Creates a scroll area for large images
		self.image_scrolly = QScrollArea( self )
		self.image_scrolly.setWidget( self.image_label )
		self.image_scrolly.setWidgetResizable( True )
		
		# Add to stack
		self.stack.addWidget( self.image_scrolly )
		
		""" Model Training Mode """
		
		self.modelTraining = ModelTrainingWidget()
		
		# Add to stack
		self.stack.addWidget( self.modelTraining )
		
		""" Setup GUI """
		
		# Centers the scroll area
		self.setCentralWidget( self.stack )
		
		# Initializes all QActions used by the application
		self.initActions()
		
		# Adds a status bar to the bottom of the application window
		self.statusBar()
		
		# Adds a menu bar at the top of the application window
		menubar = self.menuBar()

		""" Populates the menu bar with various menus and actions """
		
		# File Menu
		file_menu = menubar.addMenu( '&File' )
		
		file_menu.addAction( self.open_act )	# open
		file_menu.addSeparator()	# -------------
		file_menu.addAction( self.import_model_act )	# import model
		file_menu.addAction( self.export_model_act )	# export model
		file_menu.addSeparator()	# -------------
		file_menu.addAction( self.exit_act )	# exit
		
		'''
		# Restoration Menu
		restore_menu = menubar.addMenu( '&Restoration' )
		
		restore_menu.addAction( self.restore_act )
		'''
		
		# Adds toolbars for each mode under the menubar.
		self.toolbar_restore	= self.addToolBar( 'Toolbar Restore' )
		self.toolbar_train	= self.addToolBar( 'Toolbar Train' )
		
		self.toRestoreMode()
		
		# Adds some frequently used actions to the toolbars
		self.toolbar_restore.addAction( self.training_mode_act )
		self.toolbar_restore.addSeparator()
		self.toolbar_restore.addAction( self.restore_act )
		
		self.toolbar_train.addAction( self.restore_mode_act )
		self.toolbar_train.addSeparator()
		
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

		self.open_act	= self.initAction( 'Open', self.openImage, shortcut='Ctrl+O', status='Open Image' )
		self.import_model_act	= self.initAction( 'Import Model', self.importModel, status='Import Model' )
		self.export_model_act	= self.initAction( 'Export Model', self.exportModel, status='Export Model' )
		self.exit_act	= self.initAction( 'Exit', self.close, shortcut='Alt+F4', status='Exit Application' )
		self.restore_act	= self.initAction( 'Restore', self.restoreImage, shortcut='Ctrl+Enter', status='Restore Image' )
		
		self.restore_mode_act	= self.initAction( 'Restore Mode', self.toRestoreMode, shortcut='', status='Switch to Restore Mode' )
		self.training_mode_act	= self.initAction( 'Training Mode', self.toTrainingMode, shortcut='', status='Switch to Training Mode' )
	
	
	### Actions ###
	
	def openImage( self ):
		'''Prompts the user to select an image file and loads it into the application.'''
	
		filename = QFileDialog.getOpenFileName(	self, 'Open File',
			os.getcwd(),
			'Images (*.png *.jpg)' )
		
		read_image = FileIO.readImage( filename[0] )
		
		if read_image is not None:
			self.image = read_image
			self.image_label.setPixmap( QPixmap( self.image ) )
	
	def restoreImage( self ):
		'''Passes the current image through the restoration model, displaying the resulting restored image.'''
		
		if not self.image_label.pixmap():
			self._dialog( 'Before restoring an image, please open it using File->Open (Ctrl+O)' )
			return
		
		self._dialog( 'image restoration is not yet implemented' )
		
		pass # TODO: Implement restoreImage
		
		# output = model.toImage( model.input( model.toNdArray( self.image ) ) )
		# (or something)
	
	def importModel( self ):
		'''Prompts the user to select a model config file and loads it into the application.'''
		
		self._dialog( 'import model is not yet implemented.' )
		
		pass # TODO: Implement importModel
	
	def exportModel( self ):
		'''Prompts the user to enter a valid filename, and saves the model under that filename.'''
		
		self._dialog( 'export model is not yet implemented.' )
		
		pass # TODO: Implement exportModel
		
	
	def toRestoreMode( self ):
		'''Switches to Restore Mode for restoring images.'''
	
		self.toolbar_train.hide()
		self.toolbar_restore.show()
		
		self.stack.setCurrentIndex( 0 )
	
	def toTrainingMode( self ):
		'''Switches to Training Mode for training the model.'''
	
		self.toolbar_restore.hide()
		self.toolbar_train.show()
		
		self.stack.setCurrentIndex( 1 )
	

	
	### Helper Functions ###
	
	def _dialog( self, msg ):
		'''Displays a dialog box to the user with a message.'''
	
		dialog = QMessageBox()
		dialog.setText( msg )
		dialog.exec()
	
	def _toggleMode( self ):
		'''Toggles the current mode'''
		self.stack.setCurrentIndex( ( self.stack.currentIndex() + 1 ) % self.stack.count() )


	
if __name__ == '__main__':

	app = QApplication( sys.argv )

	# Instantiates the application window
	image_restoration_app = ImageRestorationApp()

	sys.exit( app.exec_() )
