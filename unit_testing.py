# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 21:49:19 2018

@author: Rafiya
"""

import numpy as np
import scipy as sp
import scipy.signal  # one option for a 2D convolution library
import cv2
import matplotlib.pyplot as plt
from os import path
import seam_carving as sc




img = cv2.imread("sample_image.png", cv2.IMREAD_COLOR)

image = np.atleast_3d(img).astype(np.float)

energy = sc.calculate_energy(image)

print(energy.shape)

plt.imshow(energy, cmap="gray")

energy = np.array([[0, 0, 0], [1, 1, 1], [2, 3, 4]])

cost_matrix = sc.find_seams(energy)

print(cost_matrix)



