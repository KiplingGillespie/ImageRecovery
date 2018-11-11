#! python

#Contributors:	Cody Leslie
#Last Modified:	11/11/2018
#Description:	Provide a command line interface through which to run the Image Restore Tool.
#		Should be provided command line input of the form -t directoryIn directoryOut weightOut
#		or -r imageIn imageOut weightIn. Prints "Done" when either task is completed.

import sys
from ML import Train
from Clean import Clean
from toHD5 import pairsToHD5

# Tell the user how to provide the best input
def formatPrompt(goodOption, training):
	if goodOption:
		if training:
			out = "Input should be of form -t directoryIn directoryOut weightOut"
		else:
			out = "Input should be of form -r imageIn imageOut weightIn"
	else:
		out = ("Must have command line arguments of the following forms\n"
		"-t directoryIn directoryOut weightOut 	 --- for training on a data set\n"
		"-r imageIn imageOut weightIn		 --- for restoring a specific image")
	print(out, file = sys.stderr)	

# Provide a command line interface for the Image Restore Tool
def commandUI():
	
	# If we recieved any command line arguments at all, move on to checking
	if len(sys.argv) > 1:
	
		#If training
		if sys.argv[1] == "-t":
			
			#If we have the wrong number of arguments
			if len(sys.argv) != 5:
				formatPrompt(True, True)
				return
			
			
			### INCOMPLETE
			# Check validity of directories
			
			#Convert files for training
			pairsToHD5(sys.argv[2], sys.argv[3])
			
			#Train on the set
			Train()
			
			### INCOMPLETE
			# Output the model to the location (currently only has default)
			print("Done")
		
		#If restoring
		elif sys.argv[1] == "-r":
			
			#If we have the wrong number of arguments
			if len(sys.argv) != 5:
				formatPrompt(True, False)
				return
				
			### INCOMPLETE
			# Check validity of fileIn and weightIn
			
			### INCOMPLETE
			# Clean the input image (currently only inputs from default model location)
			Clean(sys.argv[2], sys.argv[3]) #, sys.argv[4])
			print("Done")
				
		else:
			#Prompt for good input
			formatPrompt(False, False)
			return
	else:
	# Otherwise, tell the user how to give good input.
		formatPrompt(False, False)
		return

commandUI()
