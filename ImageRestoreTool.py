#! python

#Contributors:	Cody Leslie
#Last Modified:	11/1/2018
#Description:	Provide a command line interface through which to run the Image Restore Tool.
#				Should be provided command line input of the form -t directoryIn directoryOut
#				or -r imageIn imageOut weightIn. Prints the weights of the trained model in 
#				the first style and "Done" in the second to stdout.

#import FileIO
import sys

# Tell the user how to provide the best input
def formatPrompt(goodOption, training):
	if goodOption:
		if training:
			out = "Input should be of form -t directoryIn directoryOut"
		else:
			out = "Input should be of form -r imageIn imageOut weightIn"
	else:
		out = ("Must have command line arguments of the following forms\n"
		"-t directoryIn directoryOut  --- for training on a data set\n"
		"-r imageIn imageOut weightIn --- for restoring a specific image")
	print(out, file = sys.stderr)	

# Provide a command line interface for the Image Restore Tool
def commandUI():
	
	# If we recieved any command line arguments at all, move on to checking
	if len(sys.argv) > 1:
	
		#If training
		if sys.argv[1] == "-t":
			
			#If we have the wrong number of arguments
			if len(sys.argv) != 4:
				formatPrompt(True, True)
				return
			
			
			### INCOMPLETE
			# Check validity of directories
			# Start Model
			# weights = train(dirIn, dirOut)
			weights = [0.0]
			print(weights)
			
		
		#If restoring
		elif sys.argv[1] == "-r":
			
			#If we have the wrong number of arguments
			if len(sys.argv) != 5:
				formatPrompt(True, False)
				return
				
			### INCOMPLETE
			# Check validity of fileIn and weightIn
			# Start Model
			# loadWeights(weighIn)
			# restore(fileIn, fileOut)
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