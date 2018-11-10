## TRAIN Model

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import caffe


def Train(solver = "Data/solver.prototxt"):
    caffe.set_mode_cpu()
    solver = caffe.get_solver(solver)
    solver.solve();

