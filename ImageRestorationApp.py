#! python

from PyQt5.QtWidgets import	(QApplication, QMainWindow, QAction,
	QFileDialog, QMessageBox,
	QLabel, QScrollArea, QStackedWidget, QWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QStandardPaths

from ModelTrainingWidget import ModelTrainingWidget
from RestorationWidget import RestorationWidget


import sys
import os
os.chdir( QStandardPaths.writableLocation( QStandardPaths.StandardLocation.DocumentsLocation ) )
from functools import partial

#import FileIO
import QtHelper



class ImageRestorationApp( QMainWindow ):

	def __init__( self ):

		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
		
		# Enables switching between Image Restoration and Model Training GUIs
		self.stack = QStackedWidget( self )

		""" Image Restoration Mode """
		
		self.image_restoration	= RestorationWidget()
		
		""" Model Training Mode """
		
		self.model_training = ModelTrainingWidget()
		
		""" Add to Stack """
		
		self.stack.addWidget( self.image_restoration )
		self.stack.addWidget( self.model_training )
		
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
		
		self.file_menu	= menubar.addMenu( '&File' )
		
		self.file_menu.addAction( self.open_act )
		self.file_menu.addSeparator()
		self.file_menu.addAction( self.import_model_act )
		self.file_menu.addAction( self.export_model_act )
		self.file_menu.addSeparator()
		self.file_menu.addAction( self.exit_act )
		
		'''
		self.file_menu_restore = menubar.addMenu( '&File' )
		
		self.file_menu_restore.addAction( self.open_act )	# open
		self.file_menu_restore.addSeparator()	# -------------
		self.file_menu_restore.addAction( self.import_model_act )	# import model
		self.file_menu_restore.addAction( self.export_model_act )	# export model
		self.file_menu_restore.addSeparator()	# -------------
		self.file_menu_restore.addAction( self.exit_act )	# exit
		
		self.file_menu_train = menubar.addMenu( '&File' )
		
		self.file_menu_train.addAction( self.import_model_act )	# import model
		self.file_menu_train.addAction( self.export_model_act )	# export model
		self.file_menu_train.addSeparator()	# -------------
		self.file_menu_train.addAction( self.exit_act )	# exit
		'''
		
		# Adds a toolbar, and populates it with frequently used actions
		
		self.toolbar	= self.addToolBar( 'Toolbar' )
		
		self.toolbar.addAction( self.training_mode_act )
		self.toolbar.addAction( self.restore_mode_act )
		self.toolbar.addSeparator()
		self.toolbar.addAction( self.restore_act )
		self.toolbar.addAction( self.train_act )
		
		
		### Setup Window and Set Mode ###
		
		self.toRestoreMode()
		self.setGeometry( 100, 100, 800, 600 ) # X-Pos, Y-Pos, Width, Height
		self.setWindowTitle( 'Image Restoration' )
		
		self.show()
	

	def initActions( self ):
		'''Initializes each action used by the application.'''

		self.import_model_act	= QtHelper.initAction( self, 'Import Model', self.importModel, status='Import Model' )
		self.export_model_act	= QtHelper.initAction( self, 'Export Model', self.exportModel, status='Export Model' )
		self.exit_act	= QtHelper.initAction( self, 'Exit', self.close, shortcut='Alt+F4', status='Exit Application' )
		
		self.open_act	= QtHelper.initAction( self, 'Open', self.image_restoration.openImage, shortcut='Ctrl+O', status='Open Image', icon='Open Image.png' )
		self.restore_act	= QtHelper.initAction( self, 'Restore Image', self.image_restoration.restoreImage, shortcut='Ctrl+Enter', status='Restore the opened Image using the current ML Model', icon='Restore.png' )
		
		self.train_act	= QtHelper.initAction( self, 'Train Model', self.model_training.trainModel, status='Train the current ML Model using the current training and testing image sets', icon='Train Model.png' )
		
		self.restore_mode_act	= QtHelper.initAction( self, 'Restore Mode', self.toRestoreMode, shortcut='', status='Switch to Restore Mode', icon='Change Mode.png' )
		self.training_mode_act	= QtHelper.initAction( self, 'Training Mode', self.toTrainingMode, shortcut='', status='Switch to Training Mode', icon='Change Mode.png' )
	
		self.restore_file_menu_layout	= [self.open_act, '-', self.import_model_act, self.export_model_act, '-', self.exit_act]
		self.train_file_menu_layout	= [self.import_model_act, self.export_model_act, '-', self.exit_act]
		
		self.restore_toolbar_layout	= [self.training_mode_act, '-', self.restore_act]
		self.train_toolbar_layout	= [self.restore_mode_act, '-', self.train_act]
		
		#self.restore_acts	= [self.open_act, self.import_model_act, self.export_model_act, self.exit_act] + [self.training_mode_act, self.restore_act]
		#self.train_acts	= [self.import_model_act, self.export_model_act, self.exit_act] + [self.restore_mode_act, self.train_act]
		self.restore_acts	= [x for x in (self.restore_file_menu_layout + self.restore_toolbar_layout) if type(x) is QAction]
		self.train_acts	= [x for x in (self.train_file_menu_layout + self.train_toolbar_layout) if type(x) is QAction]
	
	
	### Actions ###
	
	def importModel( self ):
		'''Prompts the user to select a model config file and loads it into the application.'''
		
		QtHelper.dialog( 'import model is not yet implemented.' )
		
		# Pass model to self.model_training & self.image_restoration
		
		pass # TODO: Implement importModel
	
	def exportModel( self ):
		'''Prompts the user to enter a valid filename, and saves the model under that filename.'''
		
		QtHelper.dialog( 'export model is not yet implemented.' )
		
		pass # TODO: Implement exportModel
		
	
	def changeMode( self, restore = True ):
	
		first, second = (self.train_acts, self.restore_acts) if restore else (self.restore_acts, self.train_acts)
		for act in first:
			act.setVisible( False )
		for act in second:
			act.setVisible( True )
	
	
	def toRestoreMode( self ):
		'''Switches to Restore Mode for restoring images.'''
		
		self.changeMode( True )
		
		self.stack.setCurrentIndex( 0 )
	
	def toTrainingMode( self ):
		'''Switches to Training Mode for training the model.'''
		
		self.changeMode( False )
		
		self.stack.setCurrentIndex( 1 )
	
	
	### Events ###
	
	def keyPressEvent( self, e ):
	
		if e.key() == Qt.Key_F11:
			if self.isMaximized():
				self.showNormal()
			else:
				self.showMaximized()


	
if __name__ == '__main__':

	app = QApplication( sys.argv )

	# Instantiates the application window
	image_restoration_app = ImageRestorationApp()

	sys.exit( app.exec_() )
