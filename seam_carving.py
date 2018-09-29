# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 19:16:36 2018

@author: Rafiya
"""


import numpy as np
import scipy as sp
import scipy.signal  # one option for a 2D convolution library
import cv2


def energy_kernel():
    """Return a 5x5 generating kernel based on an input parameter (i.e., a
    square "5-tap" filter.)

    Parameters
    ----------
    a : float
        The kernel generating parameter in the range [0, 1] used to generate a
        5-tap filter kernel.

    Returns
    -------
    output : numpy.ndarray
        A 5x5 array containing the generated kernel
    """
    # DO NOT CHANGE THE CODE IN THIS FUNCTION
    kernel = np.array([-1, 1])
    return kernel
    


def calculate_energy(image, kernel=energy_kernel()):
    """
    """
    
    image = image.astype(dtype=np.float64)
    energy = []
    
    for ch in np.rollaxis(image, -1):
       
        
        #step 1: first pad the image
        image_padded = cv2.copyMakeBorder(ch,0,0,1,1,cv2.BORDER_REFLECT_101)
        image_padded = cv2.copyMakeBorder(image_padded,1,1,0,0,cv2.BORDER_REFLECT_101)
    
        #step 2: next convolve it with the kernel
        energyX = cv2.filter2D(image_padded, -1, kernel)
        energyY = cv2.filter2D(image_padded, -1, kernel.T)
        
        ##step 3: lastly, subsample it
        new_image = abs(energyX) + abs(energyY)
                
        energy.append(new_image)
    
    energy=np.array(energy)
    print(energy.shape)
    energy = np.sum(energy, axis=0)

    return energy

def find_seams(energy_matrix, count=1):
    """
    
    1. Accumulated cost matrix : 
            The value of a pixel in the accumuluated cost matrix is equal to:
            its corresponding pixel value in the energy map added to the 
            minimum of its three top neighbors (top-left, top-center, and top-right) 
            from the accumulated cost matrix. 
            
            The value of the very top row (which obviously has no rows above it) 
            of the accumulated cost matrix is equal to the energy map. 
            
            Boundary conditions in this step are also taken into consideration. 
            If a neighboring pixel is not available due to the left or right edge, 
            it is simply not used in the minimum of top neighbors calculation.
            
    2. Minimum seam by backtracing from bottom to top edge
    
    """
    
    #Step 1: Create Cost Matrix
    
    cost_matrix = energy_matrix #initialize cost_matrix to just be the energy matrix 
    
    #then we dynamically update the values
    
    m = cost_matrix.shape[0]-1
    n = cost_matrix.shape[1]-1
    
    for i in range(m+1):
        cost_matrix[i, 0] = calculate_cost(i, 0, cost_matrix, m, n)
    
    
    
    #Step 2: Find minimum seam
    

    return cost_matrix

def calculate_cost(i, j, array_ref, m, n):
    
    print(array_ref)
        
    if (i>m or i<0): #if passing one of the side edges, return some very large value
        return 100000
    elif (j==n):     #if reached the bottom row, just return original energy fxn
        return array_ref[i,j]
    else:
        return array_ref[i,j]+np.min([calculate_cost(i, j+1, array_ref, m, n), #moving straight down 
                             calculate_cost(i+1, j+1, array_ref, m, n), #moving down and to the left 
                             calculate_cost(i-1, j+1, array_ref, m, n) #moving down and to the right 
                             ])
    

def remove_seam(image, seam):
    """
    """
    

    return image