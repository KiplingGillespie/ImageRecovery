## TRAIN Model

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import caffe

caffe.set_mode_cpu()

net = caffe.Net('Data/data.prototxt', caffe.TEST)

net.forward()