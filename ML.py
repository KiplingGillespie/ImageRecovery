import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import caffe

caffe.set_mode_cpu()

net = caffe.Net('Data/data.prototxt', caffe.TEST)

net.forward()

"""im = np.array(Image.open('Data/cat_gray.jpg'))

plt.imshow(im, cmap='gray')
plt.show()

net.save('mymodel.caffemodel')

#print(net.blobs['conv'].data[0, 0])
"""
plt.imshow(net.blobs['conv'].data[0, 0], cmap='gray')
plt.show()

net.backward()

plt.imshow(net.blobs['conv'].data[0, 0], cmap='gray')
plt.show()
