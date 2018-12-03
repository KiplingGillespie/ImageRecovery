import os
import sys
import numpy as np
import math


import cv2
import caffe


def PrepImage(Image):
    ycrcb = cv2.cvtColor(Image, cv2.COLOR_RGB2YCR_CB)
    Image = ycrcb[:,:,0]

    # im_raw = cv2.resize(im_raw, (int(im_raw.shape[0]/2), int(im_raw.shape[1]/2)))
    #im_raw = im_raw.reshape((1, 1, im_raw.shape[0], im_raw.shape[1]))
    height = int(92)
    width = int(92)
    imHeight = Image.shape[0]
    imWidth = Image.shape[1]
    subrows = imHeight//height
    subcol = imWidth//width

    image_set = []
    for i in range(0, subrows):
        image_set.append([])
        for j in range(0, subcol):
            image_set[i].append(Image[j:j+height, i:i+width])

    return image_set


def Normalize(Image):
    # normalize values
    maxColor = 255
    row_sums = Image.sum(axis=1)
    Image = (Image / row_sums) * maxColor
    return Image


def Combine_Images(image_list):
    # Extract output image from net, change format to int8 and reshape
    final_image = []
    for row in image_list:
        final_image.append([])
        for image in row:
            hor1 = np.concatenate((image[0], image[1], image[2], image[3]), axis=1)
            hor2 = np.concatenate((image[4], image[5], image[6], image[7]), axis=1)
            hor3 = np.concatenate((image[8], image[9], image[10], image[11]), axis=1)
            hor4 = np.concatenate((image[12], image[13], image[14], image[15]), axis=1)

            image = np.concatenate((hor1, hor2, hor3, hor4), axis=0)
            final_image[-1].append(image)

    return final_image


def Combine_Step2(image_list):
    image = []
    for y in image_list:
        row = []
        for x in y:
            row.append(x)

        image.append(np.concatenate(row, axis=1))

    result = np.concatenate(image, axis=0)
    return result


def Perform(test_image_set, net):
    result = []
    for row in test_image_set:
        result.append([])
        for sub in row:
            # Copy input image data to net structure
            net.blobs['Input'].reshape(1, 1, sub.shape[0], sub.shape[1])
            net.blobs['Input'].data[...] = sub.reshape((1, 1, sub.shape[0], sub.shape[1]))

            # Run forward pass
            out = net.forward()
            toadd = out['deconv1'][0]
            result[-1].append(toadd)

    return result


def Clean(inputFile='Data/TrainingData/MinQF/_Page_01.jpg',
          outputFile='clean.jpg',
          model='Data/snapshot-56_12_4_iter_20.caffemodel',
          net='Data/net.prototxt',
          scale = 10):


    # Set mode to run on CPU
    caffe.set_mode_cpu()

    # Create Caffe model using pretrained model
    net = caffe.Net(net, model, caffe.TEST)

    # Input image
    im_raw = cv2.imread(inputFile)
    raw_size = im_raw.shape

    test_set = PrepImage(im_raw)

    results = Perform(test_set, net)

    results = Combine_Images(results)
    results = Combine_Step2(results)

    # normalize values
    #results = Normalize(results)
    # print(len(results))

    # mat = (mat[0, :, :]).astype('uint8')
    #results[0] = results[0].reshape(results[0].shape[0], results[0].shape[1], 1)

    cv2.imwrite(outputFile, results)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    Clean()

