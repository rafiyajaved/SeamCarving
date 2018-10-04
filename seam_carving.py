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
    cost_matrix = np.array(energy_matrix) #initialize cost_matrix to just be the energy matrix 
    #then we dynamically update the values
    m = cost_matrix.shape[0]
    n = cost_matrix.shape[1]
    for j in range(1, m):
        for k in range(n):
            print(j, k)
            if(k+1>=n):
                cost_matrix[j, k] = cost_matrix[j, k] + np.min([cost_matrix[j-1, k-1],
                                                                cost_matrix[j-1, k]])
            elif(k-1<0):
                cost_matrix[j, k] = cost_matrix[j, k] + np.min([cost_matrix[j-1, k+1],
                                                        cost_matrix[j-1, k]])
            else:
                cost_matrix[j, k] = cost_matrix[j, k] + np.min([cost_matrix[j-1, k-1], 
                                                        cost_matrix[j-1, k], 
                                                        cost_matrix[j-1, k+1]])
        
    return cost_matrix

def find_multiple_seams(cost_matrix, count=1):
    
    kseams = []
    for p in range(count):
        seam = find_minimum_seam(cost_matrix)
        cost_matrix = remove_seam(cost_matrix, seam)
        kseams.append(seam)
    
    return kseams

def find_minimum_seam(cost_matrix):
    
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
        
        
        seam.append([-w, best_column])
     
    return seam
    

def remove_seam(cost_matrix, seam):
    """
    """
    list_rows = []
    
    for point in seam:
        row = cost_matrix[point[0],:]
        new_row = np.delete(row, point[1])
        list_rows.append(new_row)
    

    return np.vstack(list_rows)
    

def calculate_energy_of_seam(cost_matrix, seam):
    """
    """
    energy = 0
    for point in seam:
        print("adding",cost_matrix[point[0], point[1]])
        energy = energy + cost_matrix[point[0], point[1]]
    return energy
    

def calculate_T(energy_matrix, r, c):
    """
    """
    
    """
    What if I pick at each point, whether to do column before row?
    """

    T = np.full((r+1,c+1), -1)
    T[0,0] = 0
    
    
    energy_matrix_col_before = np.array(energy_matrix)
    
    for column in range(1,c+1):
        #first fill out first row
        cm = compute_cost_matrix(energy_matrix_col_before)
        seam = find_minimum_seam(cm)
        seamenergy=calculate_energy_of_seam(cm, seam)
        T[0, column] = T[0, column-1] + seamenergy
        cost_matrix_col_before = remove_seam(cm, seam)

    energy_matrix_row_before = np.array(energy_matrix)
    
    energy_matrices_entire_previous_column = []

    for row in range(1,r+1):
        print(cost_matrix_row_before)
        #first fill out first row
        seam = find_minimum_horizontal_seam(cost_matrix_row_before)
        seamenergy=calculate_energy_of_seam(cost_matrix_row_before, seam)
        T[row, 0] = T[row-1, 0] + seamenergy
        cost_matrix_row_before = remove_seam(cost_matrix_row_before, seam)
        cost_matrices_entire_previous_column.append(cost_matrix_row_before)
    
    print(T)
    energy_matrix_row_before = np.array(energy_matrix)
    energy_matrix_col_before = np.array(energy_matrix)
            
    for column in range(1,c+1):
        energy_matrices_this_column=[]
        for row in range(1,r+1):
            
            #calculate expense of removing column first
            vertseam = find_minimum_vertical_seam(cost_matrix_col_before)
            column_first = T[row,column-1] + calculate_energy_of_seam(cost_matrix_col_before, vertseam)

            
            #calculate expense of rmoeving row first
            horzseam = find_minimum_horizontal_seam(cost_matrix_row_before)
            row_first = T[row-1, column] + calculate_energy_of_seam(cost_matrix_row_before, horzseam)
 
            print("vertical seam", vertseam, column_first)
            print("horizontal seam", horzseam, row_first)
            
            #compare the two paths
            if(row_first<=column_first):
                print("row first")
                T[row,column] = row_first
                cost_matrix_row_before = remove_seam(cost_matrix_row_before, horzseam)
                energy_matrices_this_column.append(cost_matrix_row_before)

            elif(column_first<=row_first):
                print("column first")
                T[row,column] = column_first
                energy_matrix_row_before = remove_seam(cost_matrix_col_before, vertseam)
                energy_matrices_this_column.append(cost_matrix_row_before)
            
            if(row<r):
                energy_matrix_col_before = energy_matrices_entire_previous_column[row+1]
        
        energy_matrices_entire_previous_column = cost_matrices_this_column
                
    print(T)
    return T

def shrink_image(image, newDimX, newDimY):
    """
    """

    return image

def expand_image(image, newDimX, newDimY):
    """
    """

    return image