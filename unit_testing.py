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

energy = energy[0:10, 0:20]


plt.imshow(energy, cmap="gray")

cost_matrix = sc.compute_cost_matrix(energy)

print("final",cost_matrix)

seam = sc.find_minimum_seam(cost_matrix)

print("seam", seam)

for point in seam:
    energy[point[0], point[1]] = 255

plt.imshow(energy, cmap="gray")




