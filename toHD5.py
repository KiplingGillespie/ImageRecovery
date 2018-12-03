#Contributors:  Cody Leslie
#Last Modified: 11/10/2018

#Based on a prototype model made available by intel at
#https://software.intel.com/en-us/articles/an-example-of-a-convolutional-neural-network-for-image-super-resolution-tutorial

import os
import sys
import numpy as np
import h5py
import cv2
from math import sqrt
import os

#Make the HD5 files for a training directory
#Assumed that all inputs have already been checked
def pairsToHD5(dirIn, dirGnd):

    #Initialize all variables and placeholders
    dirName = os.path.dirname(os.path.abspath(__file__))
    allFiles = os.listdir(dirGnd)
    numFiles = 0
	
    tempDir = os.path.join( dirName, 'temp' )
    
    #Make a temporary folder for the HD5 files if not already made
    if not os.path.exists( tempDir ):
        os.mkdir( tempDir )
    fileList = open( os.path.join( tempDir, 'train.txt' ), 'w')
    
    #For all files
    for filename in allFiles:
        
        #Read images to process
        In = cv2.imread( os.path.join( dirIn, os.path.splitext(filename)[0]+'.jpg' ) )
        Gnd = cv2.imread( os.path.join( dirGnd, filename ) )
        
        #Process each file
        toHD5(In, Gnd, os.path.join( tempDir, 'train'+str(numFiles) ) )
        numFiles += 1
        
        #Write filename to train.txt
        fileList.write( os.path.join( tempDir, 'train'+str(numFiles)+'.h5\n' ) )
        
    fileList.close()
    return


#Convert the Given Input and Ground images into an HD5 file
def toHD5(imageIn, imageGnd, outfile):
    
    #Change color-spaces to YCR_CB
    image_ycrcbIn = cv2.cvtColor(imageIn, cv2.COLOR_RGB2YCR_CB)
    image_ycrcbIn = image_ycrcbIn[:,:,0]
    image_ycrcbIn = image_ycrcbIn.reshape((image_ycrcbIn.shape[0], image_ycrcbIn.shape[1]))
    
    image_ycrcbGnd = cv2.cvtColor(imageGnd, cv2.COLOR_RGB2YCR_CB)
    image_ycrcbGnd = image_ycrcbGnd[:,:,0]
    image_ycrcbGnd = image_ycrcbGnd.reshape((image_ycrcbGnd.shape[0], image_ycrcbGnd.shape[1]))
    
    height, width = image_ycrcbGnd.shape[:2]
    #stride = int(sqrt(height*width/1024)) +1
    stride = 92
    size_ground = stride
    
    # Declare tensors to hold 1024 LR-HR subimage pairs
    input_In = np.zeros((size_ground, size_ground, 1, 1024))
    input_Gnd = np.zeros((size_ground, size_ground, 1, 1024))
    
    #Iterate over the train image using the specified stride and create LR-HR subimage pairs
    count = 0
    for i in range(0, height-size_ground+1, stride):
        for j in range(0, width-size_ground+1, stride):
            subimage_In = image_ycrcbIn[i:i+size_ground, j:j+size_ground]
            subimage_Gnd = image_ycrcbGnd[i:i+size_ground, j:j+size_ground]
            count = count + 1
            input_In[:,:,0,count-1] = subimage_In
            input_Gnd[:,:,0,count-1] = subimage_Gnd
    
    #Create an hdf5 file
    with h5py.File( outfile+'.h5', 'w' ) as H5:
        H5.create_dataset( 'Input', data=np.transpose(input_In, (3,2,1,0)) )
        H5.create_dataset( 'Ground', data=np.transpose(input_Gnd, (3,2,1,0)) )
    return

#pairsToHD5('CS 499 Training Data\\Input', 'CS 499 Training Data\\Ground')