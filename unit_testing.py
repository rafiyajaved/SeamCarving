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




### img = cv2.imread("sample_image.png", cv2.IMREAD_COLOR)

###image = np.atleast_3d(img).astype(np.float)


#energy = sc.calculate_energy(image)

#plt.imshow(energy, cmap="gray")

#cost_matrix = sc.compute_cost_matrix(energy)

#seam = sc.find_minimum_vertical_seam(cost_matrix)
#seam2 = sc.find_minimum_horizontal_seam(cost_matrix)

"""
for point in seam:
        if(point[0]>=img.shape[0] or point[1]>=img.shape[1]):
            pass
        else:
            img[point[0], point[1], 0] = np.max(img)

for point in seam2:
        if(point[0]>=img.shape[0] or point[1]>=img.shape[1]):
            pass
        else:
            img[point[0], point[1], 0] = np.max(img)

plt.imshow(img)

"""
#print(image.shape)

#for seam in seams:
#    for point in seam:
#        if(point[0]>=img.shape[0] or point[1]>=img.shape[1]):
#            pass
#        else:
#            img[point[0], point[1], 0] = np.max(img)

#plt.imshow(img)

energy_matrix = np.array([[1,2,3,4], [2, 1, 8,2], [2, 9, 6, 1]])
print(energy_matrix)

cost_matrix = sc.compute_cost_matrix(energy_matrix)

seam = sc.find_minimum_seam(cost_matrix)
for point in seam:
        print("point",energy_matrix[point[0], point[1]])
print(seam)
print(cost_matrix)
print(energy_matrix)


#E = sc.calculate_E(cost_matrix, 1, 1)



