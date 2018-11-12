import os
import sys
import numpy as np


import cv2
import caffe


def Clean(inputFile='Data/TrainingData/MinQF/_Page_01.jpg',
          outputFile = '../peppersl_clean.jpg',
          model='Data/snapshot-56_12_4_iter_1.caffemodel',
          net = 'Data/net.prototxt',
          scale = 10):

    # Create Caffe model using pretrained model
    net = caffe.Net(net, model, caffe.TEST)

    # Input image
    im_raw = cv2.imread(inputFile)


    ycrcb = cv2.cvtColor(im_raw, cv2.COLOR_RGB2YCR_CB)
    im_raw = ycrcb[:,:,0]

    im_raw = cv2.resize(im_raw, (int(im_raw.shape[0]/2), int(im_raw.shape[1]/2)))
    im_raw = im_raw.reshape((1, 1, im_raw.shape[0], im_raw.shape[1]))

    # Set mode to run on CPU
    caffe.set_mode_cpu()

    # Copy input image data to net structure
    net.blobs['Input'].reshape(1, 1, im_raw.shape[2], im_raw.shape[3])
    net.blobs['Input'].data[...] = im_raw

    # Run forward pass
    out = net.forward()

    # Extract output image from net, change format to int8 and reshape
    mat = out['deconv1'][0]
    mat = (mat[0, :, :]).astype('uint8')

    #mat = mat.reshape(mat.shape[2], mat.shape[3])
    cv2.imwrite('peppersl_clean.jpg', mat)

    #output cleaned image.

if __name__ == "__main__":
    Clean()