import os
import sys
import numpy as np


import cv2
import caffe


def Clean(inputFile='../peppers.jpg', outputFile = '../peppersl_clean.jpg', net = '../Data/net.prototxt',
          model='../Data/snapshot-56_12_4_iter_2.caffemodel'):

    # Create Caffe model using pretrained model
    net = caffe.Net(net, model, caffe.TRAIN)

    # Input image
    im_raw = cv2.imread(inputFile)

    # Set mode to run on CPU
    caffe.set_mode_cpu()

    # Copy input image data to net structure
    net.blobs['Input'].data[...] = im_raw

    # Run forward pass
    out = net.forward()

    # Extract output image from net, change format to int8 and reshape
    mat = out['deconv1'][0]
    mat = (mat[0, :, :]).astype('uint8')

    #output cleaned image.
    cv2.imshow("image", mat)
    cv2.imwrite(outputFile, mat)

    cv2.waitKey()

if __name__ == "__main__":
    Clean()