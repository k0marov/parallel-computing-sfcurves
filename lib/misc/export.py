import numpy
import numpy as np

def save_2d_array(a, path):
    numpy.savetxt(path, a.astype(int), fmt='%u')
