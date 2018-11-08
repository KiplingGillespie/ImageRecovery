#! python

from PyQt5.QtWidgets import	(QWidget, QListWidget, QListWidgetItem,
	QFileDialog, QMessageBox, QToolButton,
	QLabel, QToolBar, QAction,
	QVBoxLayout, QBoxLayout)
from PyQt5.QtGui import	QIcon
from PyQt5.QtCore import	Qt

import os
import FileIO


class ImageDump( QWidget ):

	def __init__( self, parent, title ):
	
		super().__init__( parent )
		
		#self.setAcceptDrops( True )
		
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
		self.list.setSelectionMode( self.list.ExtendedSelection )
		vbox.addWidget( self.list )
		
		### Put contents in outer toolLayout ###
		
		toolLayout.addLayout( vbox )
		toolLayout.setDirection( QBoxLayout.BottomToTop )
		
		### Tools ###
		
		cwd	= os.path.abspath( os.path.dirname( __file__ ) )
		icons	= os.path.join( cwd, 'icons' )
		
		select_all_act	= QAction( QIcon(os.path.join( icons, 'Select All (2).png' )), 'Select All', self )
		select_all_act.setStatusTip( 'Select all images in an image set' )
		select_all_act.triggered.connect( self.selectAll )
		toolbar.addAction( select_all_act )

		toolbar.addSeparator()
		
		open_act	= QAction( QIcon(os.path.join( icons, 'Images.png' )), 'Add Images', self )
		open_act.setStatusTip( 'Add images to an image set' )
		open_act.triggered.connect( self.selectImages )
		toolbar.addAction( open_act )
		
		remove_act	= QAction( QIcon(os.path.join( icons, 'Delete.png' )), 'Remove Selected Images', self )
		remove_act.setStatusTip( 'Remove selected images from an image set' )
		remove_act.triggered.connect( self.removeSelected )
		toolbar.addAction( remove_act )
	
	def addItem( self, text ):
		'''Adds a new QListWidgetItem with label "text".'''
		if len( self.list.findItems( text, Qt.MatchCaseSensitive ) ) == 0:
			item = QListWidgetItem( text )
			
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
	
		vbox = QVBoxLayout()
		
		self.training_set	= ImageDump( self, 'Training Set' )
		self.testing_set	= ImageDump( self, 'Testing Set' )
		self.swap_button	= QToolButton( self )
		
		cwd	= os.path.abspath( os.path.dirname( __file__ ) )
		icons	= os.path.join( cwd, 'icons' )
		
		swap_act	= QAction( QIcon(os.path.join( icons, 'Swap.png' )), 'Swap Selected Images', self )
		swap_act.setStatusTip( 'Swap selected images between image sets' )
		swap_act.triggered.connect( self.swapSelectedImages )
		self.swap_button.setDefaultAction( swap_act )
		
		vbox.addWidget( self.training_set )
		
		inner_vbox = QVBoxLayout()
		inner_vbox.setAlignment( Qt.AlignCenter )
		inner_vbox.addWidget( self.swap_button )
		vbox.addLayout( inner_vbox )
		
		vbox.addWidget( self.testing_set )
		
		self.setLayout( vbox )
	
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