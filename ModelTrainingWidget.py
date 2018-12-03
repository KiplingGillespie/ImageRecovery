#! python

from PyQt5.QtWidgets import	(QWidget, QListWidget, QListWidgetItem,
	QFileDialog, QMessageBox, QToolButton,
	QLabel, QSplitter, QTextEdit, QFrame, QLineEdit,
	QToolBar, QAction,
	QVBoxLayout, QHBoxLayout, QBoxLayout)
from PyQt5.QtGui import	QIcon
from PyQt5.QtCore import	Qt, QSize

import os
import FileIO
import QtHelper
import toHD5
import ML
import Clean


class ImageDump( QWidget ):

	def __init__( self, parent, title ):
	
		super().__init__( parent )
		
		cwd	= os.path.abspath( os.path.dirname( __file__ ) )
		self._icons_path	= os.path.join( cwd, 'icons' )
		
		self.initUI( title )
	
	def initUI( self, title ):
	
		### Add toolbar to widget ###
		
		toolLayout	= QBoxLayout( QBoxLayout.TopToBottom, self )
		toolLayout.setContentsMargins( 0, 0, 0, 0 )
		
		toolbar	= QToolBar()
		toolLayout.addWidget( toolbar )
		
		### Add contents ###
	
		vbox = QVBoxLayout()
	
		self.label = QLabel( self )
		self.label.setText( title )
		vbox.addWidget( self.label )
		
		self.list = QListWidget( self )
		self.list.setSelectionMode( self.list.ExtendedSelection ) #MultiSelection?
		self.list.setIconSize( QSize( 60, 60 ) )
		#self.list.setFlow( QListWidget.LeftToRight )
		#self.list.setResizeMode( QListWidget.Adjust ) # TODO: Finish QListWidget settings
		#self.list.setSpacing( 2 )
		#self.list.setViewMode( QListWidget.IconMode )
		vbox.addWidget( self.list )
		
		### Put contents in outer toolLayout ###
		
		toolLayout.addLayout( vbox )
		toolLayout.setDirection( QBoxLayout.BottomToTop )
		
		### Tools ###
		
		cwd	= os.path.abspath( os.path.dirname( __file__ ) )
		icons	= os.path.join( cwd, 'icons' )
		
		select_all_act	= QtHelper.initAction( self, 'Select All', self.selectAll, status='Select all images in the image set', icon='Select All.png' )
		toolbar.addAction( select_all_act )

		toolbar.addSeparator()
		
		open_act	= QtHelper.initAction( self, 'Add Images', self.selectImages, status='Add images to the image set', icon='Images.png' )
		toolbar.addAction( open_act )
		
		remove_act	= QtHelper.initAction( self, 'Remove Selected Images', self.removeSelected, status='Remove selected images from the image set', icon='Delete.png' )
		toolbar.addAction( remove_act )
	
	
	def addItem( self, text ):
		'''Adds a new QListWidgetItem with label "text".'''
		if len( self.list.findItems( text, Qt.MatchCaseSensitive ) ) == 0:
			item = QListWidgetItem( text )
			
			item.setIcon( QIcon( text ) )
			
			self.list.addItem( item )
	
	def removeItem( self, text ):
		'''Remove all QListWidgetItems with label "text" (there should only ever be 1).'''
		for i in range(self.list.count() - 1, -1, -1):
			it = self.list.item(i)
			
			if it.text() == text:
				self.list.takeItem( i )
	
	def addItems( self, texts ):
		'''Adds a QListWidgetItem labelled by each string in [texts]. Selects the added items.'''
		self.list.clearSelection()
		for text in texts:
			self.addItem( text )
			self.list.item(self.list.count()-1).setSelected( True )
		self.list.sortItems()
	
	def removeItems( self, texts ):
		'''Removes all items with labels contained in [texts].'''
		for i in range(self.list.count() - 1, -1, -1):
			it = self.list.item(i)
			
			if it.text() in texts:
				self.list.takeItem( i )
	
	def getSelected( self ):
		'''Returns a list of text labels corresponding to the currently selected items.'''
		return [it.text() for it in list(self.list.selectedItems())]
	
	def removeSelected( self ):
		'''Removes the items currently selected from the QListWidget.'''
		selected = self.getSelected()
		if len(selected) == 0:
			return
		
		msgBox = QMessageBox()
		msgBox.setText( 'Are you sure you want to remove the selected images?' )
		msgBox.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel )
		msgBox.setDefaultButton( QMessageBox.Cancel )
		pressed = msgBox.exec_()
		
		if pressed == QMessageBox.Ok:
			for text in self.getSelected():
				self.removeItem( text )
	
	def selectAll( self ):
		'''Selects all items in the QListWidget.'''
		if len(self.list.selectedItems()) == self.list.count():
			self.list.clearSelection()
		else:
			self.list.selectAll()

	def selectImages( self ):
		'''Prompts the user for images and adds them to the current set.'''
		
		dialog = QFileDialog( self, caption = 'Open Images', directory = os.getcwd(), filter = 'Images (*.png *.jpg)' )
		dialog.setFileMode( QFileDialog.ExistingFiles )
		
		if dialog.exec_():
			filenames = dialog.selectedFiles()
		else:
			filenames = []
		
		self.addItems( filenames )



class ModelTrainingWidget( QWidget ):

	def __init__( self ):
	
		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
	
		### Set up Splitter ###
		
		splitter_box	= QVBoxLayout()
		splitter = QSplitter( Qt.Horizontal )
		splitter_box.addWidget( splitter )
		
		### Left of Splitter ###
		
		left_vbox	= QVBoxLayout()
		
		console	= QTextEdit( self )
		console.setReadOnly( True )
		
		left_vbox.addWidget( console )
		
		### Right of Splitter ###
	
		right_vbox = QVBoxLayout()
		
		'''
		self.training_set	= ImageDump( self, 'Training Set' )
		self.testing_set	= ImageDump( self, 'Testing Set' )
		self.swap_button	= QToolButton( self )
		
		cwd	= os.path.abspath( os.path.dirname( __file__ ) )
		icons	= os.path.join( cwd, 'icons' )
		
		swap_act	= QtHelper.initAction( self, 'Swap Selected Images', self.swapSelectedImages, status='Swap selected images between image sets', icon='Swap.png' )
		self.swap_button.setDefaultAction( swap_act )
		
		right_vbox.addWidget( self.training_set )
		
		inner_vbox = QVBoxLayout()
		inner_vbox.setAlignment( Qt.AlignCenter )
		inner_vbox.addWidget( self.swap_button )
		right_vbox.addLayout( inner_vbox )
		
		right_vbox.addWidget( self.testing_set )
		'''

		comp_hbox = QHBoxLayout()
		comp_hbox.addWidget( QLabel( 'Compressed Input Directory: ' ) )
		self.comp_dir	= QLineEdit( '' )
		comp_hbox.addWidget( self.comp_dir )
		
		ground_hbox	= QHBoxLayout()
		ground_hbox.addWidget( QLabel( 'Ground Truth Directory: ' ) )
		self.ground_dir	= QLineEdit( '' )
		ground_hbox.addWidget( self.ground_dir )
		
		right_vbox.addLayout( comp_hbox )
		right_vbox.addLayout( ground_hbox )

		
		### Plug into Splitter ###
		
		left_frame	= QFrame( self )
		left_frame.setFrameShape( QFrame.StyledPanel )
		left_frame.setLayout( left_vbox )
		
		right_frame	= QFrame( self )
		right_frame.setFrameShape( QFrame.StyledPanel )
		right_frame.setLayout( right_vbox )
		
		splitter.addWidget( left_frame )
		splitter.addWidget( right_frame )
		splitter.setStretchFactor( 0, 2 )
		splitter.setStretchFactor( 1, 1 )
		
		self.setLayout( splitter_box )
	
	def swapSelectedImages( self ):
		'''Swaps the selected items in the training set and the test set.'''
	
		training_swap	= self.training_set.getSelected()
		testing_swap	= self.testing_set.getSelected()

		if len(training_swap) + len(testing_swap) == 0:
			return
		
		msgBox = QMessageBox()
		msgBox.setText( 'Are you sure you want to swap the selected images?' )
		msgBox.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel )
		msgBox.setDefaultButton( QMessageBox.Cancel )
		pressed = msgBox.exec_()
		
		if pressed == QMessageBox.Ok:
		
			self.training_set.removeItems( training_swap )
			self.testing_set.removeItems( testing_swap )
		
			self.training_set.addItems( testing_swap )
			self.testing_set.addItems( training_swap )
	
	
	### Actions ###
	
	def trainModel( self ):
		'''Trains the model using the current training and testing image sets.'''
		
		#QtHelper.dialog( 'model training is not yet implemented' )
		
		toHD5.pairsToHD5( self.comp_dir.text(), self.ground_dir.text() )
		
		ML.Train()