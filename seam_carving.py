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

def compute_cost_matrix(energy_matrix):
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
    
    #Step 1: Create Accumulated Cost Matrix
    cost_matrix = energy_matrix #initialize cost_matrix to just be the energy matrix 
    #then we dynamically update the values
    m = cost_matrix.shape[0]-1
    n = cost_matrix.shape[1]-1
    for k in range(n+1):
        print(k)
        cost_matrix[0, k] = calculate_cost(0, k, cost_matrix, m, n)
        
    return cost_matrix

def calculate_cost(i, j, array_ref, m, n):
    
    
        
    if (j>n or j<0): #if passing one of the side edges, return some very large value
        return 100000
    elif (i==m):     #if reached the bottom row, just return original energy fxn
        return array_ref[i,j]
    else:
        return array_ref[i,j]+np.min([calculate_cost(i+1, j, array_ref, m, n), #moving straight down 
                             calculate_cost(i+1, j-1, array_ref, m, n), #moving down and to the left 
                             calculate_cost(i+1, j+1, array_ref, m, n) #moving down and to the right 
                             ])

def find_minimum_seam(cost_matrix, count=1):
    
    columns = cost_matrix.shape[1]-1
    rows = cost_matrix.shape[0]-1
    seam = []
    best_column = np.argmin(cost_matrix[rows, :])
    for w in range(-rows, 1):
        minimum = cost_matrix[-w, best_column]
        if best_column+1<=columns and cost_matrix[-w, best_column+1]<minimum:
            minimum = cost_matrix[-w,best_column+1]
            best_column = best_column+1
        if best_column-1>=0 and cost_matrix[-w, best_column-1]<minimum:
            minimum = cost_matrix[-w, best_column-1]
            best_column = best_column-1
        
        print(best_column)
        
        seam.append([-w, best_column])
     
    return seam
    

def remove_seam(image, seam):
    """
    """
    

    return image