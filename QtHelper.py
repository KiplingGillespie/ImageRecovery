#! python


import os

from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon, QImage

'''
import cv2
import numpy as np
'''

def initAction( self, label, trigger, shortcut = None, status = None, icon = None ):
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
		
	cwd	= os.path.abspath( os.path.dirname( __file__ ) )
	icons_path	= os.path.join( cwd, 'icons' )
	
	icon = QIcon('') if icon is None else QIcon(os.path.join( icons_path, icon ))
		
	act = QAction( icon, label, self )
	if shortcut:
		act.setShortcut( shortcut )
	if status:
		act.setStatusTip( status )
	act.triggered.connect( trigger )
	return act


def dialog( msg ):
	'''Displays a dialog box to the user with a message.'''
	
	dialog = QMessageBox()
	dialog.setText( msg )
	dialog.exec()


'''
def toOpenCvImage( self, q_image ):

	q_image	= q_image.convertToFormat( QImage.Format_RGB32 )
	
	width	= q_image.width()
	height	= q_image.height()
	
	ptr	= q_image.bits()
	ptr.setsize( q_image.byteCount() )
	arr	= np.array( ptr ).reshape( height, width, 4 )
	
	return arr
'''