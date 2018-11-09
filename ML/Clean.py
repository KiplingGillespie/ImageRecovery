####### VERY MUCH WORK IN PROGRESS


import os
import sys
import numpy as np

# Set up caffe root directory and add to path
caffe_root = '$APPS/caffe/'
sys.path.insert(0, caffe_root + 'python')
sys.path.append('opencv-2.4.13/release/lib/')

import cv2
import caffe

# Parameters
scale = 3

# Create Caffe model using pretrained model
net = caffe.Net(caffe_root + 'FSRCNN_predict.prototxt',
                caffe_root + 'examples/FSRCNN/RESULTS/FSRCNN-56_12_4_iter_300000.caffemodel', caffe.TRAIN)

# Input directories
input_dir = caffe_root + 'examples/SRCNN/DATA/Set5/'

# Input ground truth image
im_raw = cv2.imread(caffe_root + '/examples/SRCNN/DATA/Set5/butterfly.bmp')

# Change format to YCR_CB
ycrcb = cv2.cvtColor(im_raw, cv2.COLOR_RGB2YCR_CB)
im_raw = ycrcb[:, :, 0]
im_raw = im_raw.reshape((im_raw.shape[0], im_raw.shape[1], 1))

# Blur image and resize to create input for network
im_blur = cv2.blur(im_raw, (4, 4))
im_small = cv2.resize(im_blur, (int(im_raw.shape[0] / scale), int(im_raw.shape[1] / scale)))

im_raw = im_raw.reshape((1, 1, im_raw.shape[0], im_raw.shape[1]))
im_blur = im_blur.reshape((1, 1, im_blur.shape[0], im_blur.shape[1]))
im_small = im_small.reshape((1, 1, im_small.shape[0], im_small.shape[1]))

im_comp = im_blur
im_input = im_small

# Set mode to run on CPU
caffe.set_mode_cpu()

# Copy input image data to net structure
c1, c2, h, w = im_input.shape
net.blobs['data'].data[...] = im_input

# Run forward pass
out = net.forward()

# Extract output image from net, change format to int8 and reshape
mat = out['conv3'][0]
mat = (mat[0, :, :]).astype('uint8')

im_raw = im_raw.reshape((im_raw.shape[2], im_raw.shape[3]))
im_blur = im_blur.reshape((im_blur.shape[2], im_blur.shape[3]))
im_comp = im_blur.reshape((im_comp.shape[2], im_comp.shape[3]))

# Display original (ground truth), blurred and restored images
cv2.imshow("image", im_raw)
cv2.imshow("image2", im_comp)
cv2.imshow("image3", mat)
cv2.waitKey()

cv2.destroyAllWindows()