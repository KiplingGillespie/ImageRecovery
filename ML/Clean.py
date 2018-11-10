import os
import sys
import numpy as np

"""# Set up caffe root directory and add to path
caffe_root = '$APPS/caffe/'
sys.path.insert(0, caffe_root + 'python')
sys.path.append('opencv-2.4.13/release/lib/')"""

import cv2
import caffe


def Clean(inputFile='peppers.jpg', outputFile = 'peppersl_clean.jpg', net = './Data/net.prototxt',
          model='../Data/snapshot-56_12_4_iter_5000.caffemodel'):

    # Create Caffe model using pretrained model
    net = caffe.Net(net, model, caffe.TRAIN)

    # Input image
    im_raw = cv2.imread(inputFile)

    # Set mode to run on CPU
    caffe.set_mode_cpu()

    # Copy input image data to net structure
    c1, c2, h, w = im_input.shape
    net.blobs['data'].data[...] = im_raw

    # Run forward pass
    out = net.forward()

    # Extract output image from net, change format to int8 and reshape
    mat = out['deconv1'][0]
    mat = (mat[0, :, :]).astype('uint8')

    #output cleaned image.
    cv2.imwrite(outputFile)

    cv2.waitKey()

