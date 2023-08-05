#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:54:05 2019

@author: jlb269
"""

import cv2
import math
import numpy as np
from scipy import ndimage
from scipy import stats as st
import skimage.filters as filters
from scipy.optimize import fmin_powell
from operator import attrgetter
from pyhull import qconvex

# Creating a binary image mask
def Mask(img,imgtype=''):
    """Creates a mask of the cell area.

    Thresholds the image to create a binary mask, with options for images
    with a gradient or low contrast.

    Args:
        img (numpy.ndarray): An image array
        imgtype (str):  'UVF' UV Fluorescence Image
                        'gradient' for unequal intensity across the image
                        'lowcon' low contrast between cell and background
                            or PL images without background subtraction
    Returns:
        numpy.ndarray
    """
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    if 'UVF' in imgtype:
        img_gray = cv2.bitwise_not(img_gray) # For UVF images
    if 'gradient' in imgtype:
        img_gray = (img_gray)**(1/.35)
    if 'lowcon' in imgtype:
        img_gray = (img_gray)**(1.6)
    grayThreshold = filters.threshold_otsu(img_gray)
    mask = img_gray>grayThreshold
    mask = mask.astype(np.uint8)
    kernel = np.ones((5,5),np.uint8)
    mask2 = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask = cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernel)
    return mask

#Image rotation by line detection and measurement
def RotateImage(img,imgtype=''):
    """Performs rotation of an image.

    Finds lines in cell or module image and orients
    the image normal to the frame.

    Args:
        img (numpy.ndarray): An image array
        imgtype (str):  'UVF' UV Fluorescence Image
                        'gradient' for unequal intensity across the image
                        'lowcon' low contrast between cell and background
                            or PL images without background subtraction
    Returns:
        numpy.ndarray
    """
    mask = Mask(img,imgtype)
    kernel = np.ones((5,5),np.uint8)
    edges = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,kernel)
    lines = []
    #detecting cell edges and busbars as lines
    lines = cv2.HoughLinesP(edges,rho = 1, theta = math.pi/180,threshold = int(mask.shape[0]/75), minLineLength = int(mask.shape[0]/15), maxLineGap = mask.shape[0]/25)  
    if lines is None:
        cropped_img = img
    else:
        angles = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                angle = math.degrees(math.atan2(y2-y1, x2-x1))
                if angle < -45:
                    angle += 90
                elif angle > 45:
                    angle -= 90
                angles.append(angle)
        median_angle = np.median(angles)
        img_rotated = ndimage.rotate(img, median_angle)
        img_gray = cv2.cvtColor(img_rotated,cv2.COLOR_BGR2GRAY)
        mask = img_gray>0
        m,n = img_gray.shape
        top, bottom = mask[0,:], mask[-1,:]
        # Removing black pixels that were added in rotation
        if median_angle>0:
            col_end = n - top[::-1].argmax() - 1
            col_start = bottom.argmax()
            mask2 = mask[:,col_start:col_end]
            left,right = mask2[:,0],mask2[:,-1]        
            row_start = left.argmax()
            row_end = m - right[::-1].argmax() - 1
        elif median_angle<0:
            col_end = n - bottom[::-1].argmax() - 1
            col_start = top.argmax()
            mask2 = mask[:,col_start:col_end]
            left,right = mask2[:,0],mask2[:,-1]        
            row_start = right.argmax()
            row_end = m - left[::-1].argmax() - 1
        else:
            row_start, row_end, col_start, col_end = 0,m-1,0,n-1
        cropped_img = img_rotated[row_start:row_end,col_start:col_end]    
    return cropped_img

#Extracting individual cells
def CellExtract(img, numCols, numRows,imgtype=''):
    """Performs extraction of individual cells.

    Finds lines in cell or module image and orients
    the image normal to the frame.

    Args:
        img (numpy.ndarray): An image array
        numCols (int): number of cells across in module image
        numRows (int): number of cells down in module image
        imgtype (str):  'UVF' UV Fluorescence Image
                        'gradient' for unequal intensity across the image
                        'lowcon' low contrast between cell and background
                            or PL images without background subtraction
    Returns:
        list of numpy.ndarrays
    """
    mask = Mask(img,imgtype)
    cols = np.any(mask,axis=0)
    rows = np.any(mask,axis=1)
    xmin,xmax = min(np.where(cols)[0]),max(np.where(cols)[0])
    ymin,ymax = min(np.where(rows)[0]),max(np.where(rows)[0])
    # Detecting rows and columns of the module
    colsums = np.sum(mask,axis=0)
    cellwidth = (xmax-xmin)/numCols
    midpts = [int(i*cellwidth+xmin) for i in range(1,numCols)]
    xcuts = [np.median(np.where(colsums[int(midpt-cellwidth/5):int(midpt+cellwidth/5)] == min(colsums[int(midpt-cellwidth/5):int(midpt+cellwidth/5)]))[0])+int(midpt-cellwidth/5) for midpt in midpts]
    row_ch_pts = [0] + list(map(int,xcuts)) + [len(cols)]
    rowsums = np.sum(mask,axis=1)
    cellheight = (ymax-ymin)/numRows
    hmidpts = [int(i*cellheight+ymin) for i in range(1,numRows)]
    ycuts = [np.median(np.where(rowsums[int(midpt-cellheight/5):int(midpt+cellheight/5)] == min(rowsums[int(midpt-cellheight/5):int(midpt+cellheight/5)]))[0])+int(midpt-cellheight/5) for midpt in hmidpts]
    col_ch_pts = [0] + list(map(int,ycuts)) + [len(rows)]
    # Separating the module into cell arrays
    cellarrays = []
    for i in range(numRows):
        for j in range(numCols):
            result = img[col_ch_pts[i]:col_ch_pts[i+1],row_ch_pts[j]:row_ch_pts[j+1]]
            cellarrays.append(result)
    return cellarrays

# Planar Indexing an image by finding the smallest bounding 4-gon
def PlanarIndex(img,imgtype=''):
    """Performs re-orientation of module in frame.

    Broadly, this function performs tasks of filtering, edge detection, 
    corner detection, perspective transformation.

    Args:
        img (numpy.ndarray): An image array
    Returns:
        list of numpy.ndarray
    """    
    mask = Mask(img,imgtype)

    # Getting the approximate size of the image
    hullDims = mask.shape
    if any(mask[0,:]==True):
        mask = np.concatenate([np.zeros((hullDims[0],10),dtype='uint8'),mask],axis=1)
        img = np.concatenate([np.zeros((hullDims[0],10,3),dtype='uint8'),img],axis=1)
        hullDims = mask.shape
    if any(mask[-1,:]==True):
        mask = np.concatenate([mask,np.zeros((hullDims[0],10),dtype='uint8')],axis=1)
        img = np.concatenate([img,np.zeros((hullDims[0],10,3),dtype='uint8')],axis=1)
        hullDims = mask.shape
    if any(mask[:,0]==True):
        mask = np.concatenate([np.zeros((10,hullDims[1]),dtype='uint8'),mask],axis=0)
        img = np.concatenate([np.zeros((10,hullDims[1],3),dtype='uint8'),img],axis=0)
        hullDims = mask.shape
    if any(mask[:,-1]==True):
        mask = np.concatenate([mask,np.zeros((10,hullDims[1]),dtype='uint8')],axis=0)
        img = np.concatenate([img,np.zeros((10,hullDims[1],3),dtype='uint8')],axis=0)
        hullDims = mask.shape
    for i in range(hullDims[0]):
        row = mask[i,:]
        if any(row == True):
            startRow = i
            break
    for i in reversed(range(hullDims[0])):
        row = mask[i,:]
        if any(row == True):
            endRow = i
            break
    for i in range(hullDims[1]):
        col = mask[:,i]
        if any(col == True):
            startCol = i
            break
    for i in reversed(range(hullDims[1])):
        col = mask[:,i]
        if any(col == True):
            endCol = i
            break
    midRows = int((endRow + startRow)/2)
    midCols = int((endCol + startCol)/2)
    
    maskpoints = np.column_stack(np.nonzero(mask))
    # performing the convex hull and merging facets with less than .5% change in slope
    vertices = qconvex('A0.99995 PM50 i',maskpoints)
    vertarray = np.zeros((len(vertices),2),dtype=int)
    for i in range(len(vertices)-1):
        vertarray[i+1]=list(map(int,vertices[i+1].split(' ')))
    vert = maskpoints[vertarray]
    
    # Classifying facets into 4 sides
    top = []
    bottom = []
    left = []
    right = []
    for i in range(len(vert)):
        y,x = vert[i].T
        if (abs(y[0]-y[1])<abs(x[0]-x[1])): #horizontal
            if y[0] < midRows:
                top.append(vert[i])
            elif y[0] > midRows:
                bottom.append(vert[i])
        elif (abs(y[0]-y[1])>abs(x[0]-x[1])): #vertical
            if x[0] < midCols:
                left.append(vert[i])
            elif x[0] > midCols:
                right.append(vert[i])
    # Getting the longest facet for each side
    points = []
    for side in (top,left,bottom,right):
        lengths = []
        for i in range(len(side)):
            y,x=side[i].T
            lengths.append(np.sqrt(abs(y[0]-y[1])**2+abs(x[0]-x[1])**2))
        points.append(side[lengths.index(max(lengths))])
    # Finding intercepts of the 4 facets
    intercepts = []
    for j in ((0,1),(1,2),(2,3),(3,0)):
        y1, x1 = points[j[0]].T.astype(float)
        y2, x2 = points[j[1]].T.astype(float)
        slopeh, inth = attrgetter('slope','intercept')(st.linregress(x1,y1))
        if x2[0]==x2[1]:
            x=x2[0]
        else:
            slopev, intv = attrgetter('slope','intercept')(st.linregress(x2,y2))
            x=(intv - inth)/(slopeh - slopev)
        y= slopeh*x + inth
        intercepts.append([x,y])
    intercepts = np.asarray(intercepts).astype(int)
    x,y = intercepts.T
    # Defining the output dimensions
    xdim = int(np.mean((x[3],x[2]))-np.mean((x[0],x[1])))
    ydim = int(np.mean((y[2],y[1]))-np.mean((y[3],y[0])))
    # Defining the perspective transform
    pts1 = np.float32([[x[0],y[0]],[x[3],y[3]],[x[2],y[2]],[x[1],y[1]]])
    pts2 = np.float32([[0,0],[xdim,0],[xdim,ydim],[0,ydim]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    transformedImg = cv2.warpPerspective(img,M,(xdim,ydim))
    return transformedImg

# Error function for lens distortion detection
def GetLMError(x, *args):
    """Error function for detecting lens distortion using the image mask
        Called by autoLensCorrect function
    """        
    n,f = x
    mask = args[0]
    lc = lensCorrect(mask, n, f)
    m=int(mask.shape[0]/40)
    kernel = np.ones((m,m),np.uint8)
    ImgHull = cv2.morphologyEx(lc,cv2.MORPH_CLOSE,kernel)

    hullDims = ImgHull.shape

    for i in range(hullDims[0]):
        row = ImgHull[i,:]
        if any(row == True):
            startRow = i
            break
    for i in reversed(range(hullDims[0])):
        row = ImgHull[i,:]
        if any(row == True):
            endRow = i
            break
    for i in range(hullDims[1]):
        col = ImgHull[:,i]
        if any(col == True):
            startCol = i
            break
    for i in reversed(range(hullDims[1])):
        col = ImgHull[:,i]
        if any(col == True):
            endCol = i
            break
    midRows = int((endRow + startRow)/2)
    midCols = int((endCol + startCol)/2)
    imgRow = endRow - startRow
    imgCol = endCol - startCol
    
    ratio = 0.45
    rowMargin = int(imgRow*ratio)
    rowSampling = range((midRows-rowMargin),(midRows+rowMargin), int((rowMargin*2)/100))
    colMargin = int(imgCol*ratio)
    colSampling = range((midCols-colMargin),(midCols+colMargin), int((colMargin*2)/100))

    leftVector = []
    rightVector = []
    ImgHull = ImgHull.astype(int)
    for n in rowSampling:
        vector = ImgHull[n,:]
        for i in range(len(vector)-1):
            if vector[i] == 0:
                if vector[i+1] == 1:
                    leftVector.append(i)
            if vector[i] == 1:
                if vector[i+1] == 0:
                    rightVector.append(i+1)

    left_std_err = attrgetter('stderr')(st.linregress(rowSampling,leftVector))
    right_std_err = attrgetter('stderr')(st.linregress(rowSampling, rightVector))

    topVector = []
    bottomVector = []
    ImgHull = ImgHull.astype(int)
    for n in colSampling:
        vector = ImgHull[:,n]
        vec_flag = True
        for i in range(len(vector)-1):
            if vector[i] == 0:
                if vector[i+1] == 1:
                    topVector.append(i)
                elif vector[0] == 1 and vec_flag == True:
                    topVector.append(0)
                    vec_flag = False
            if vector[i] == 1:
                if vector[i+1] == 0:
                    bottomVector.append(i+1)
    top_std_err = attrgetter('stderr')(st.linregress(colSampling, topVector))
    bot_std_err = attrgetter('stderr')(st.linregress(colSampling, bottomVector))
    
    return left_std_err+right_std_err+top_std_err+bot_std_err

# Lens distortion correction
def lensCorrect(img,n,f):
    """Removes barrel or pincushion distortion from an image

    Uses input parameters to remove lens distortion.
    Input parameters can be found with pipelines.GetLensCorrectParams function

    Args:
        img (numpy.ndarray): input image array
        n (float): barrel distortion factor
        f (float): lens focal length

    Returns:
        numpy.ndarray: array of the lens corrected image

    """  
    width  = img.shape[1]
    height = img.shape[0]
    # TODO: add your coefficients here!
    k1 = -n*1e-7 # negative to remove barrel distortion -1.0e-6 is ok
    k2 = 0.0;
    p1 = 0;
    p2 = 0.0;
    distCoeff = np.zeros((4,1),np.float64)
    distCoeff[0,0] = k1;
    distCoeff[1,0] = k2;
    distCoeff[2,0] = p1;
    distCoeff[3,0] = p2;
    # assume unit matrix for camera
    cam = np.eye(3,dtype=np.float32)
    cam[0,2] = width/2.0  # define center x
    cam[1,2] = height/2.0 # define center y
    cam[0,0] = f        # define focal length x
    cam[1,1] = f        # define focal length y
    # here the undistortion will be computed
    return cv2.undistort(img,cam,distCoeff)

def autoLensCorrect(mask):
    """Obtains lens distortion correction parameters for an image mask

    Uses the GetLMError function to find optimal n, f based on error of linear 
    fitting on sides of convex hull.
    Best results on module images without darkened cells or dark cell edges.
    Recommended to find n,f on subset of images, then apply to a larger dataset.
    
    Args:
        img (numpy.ndarray): input image array

    Returns:
        n (float): barrel distortion factor
        f (float): lens focal length

    """  
    n,f = fmin_powell(GetLMError,[1.,10.],args=(mask,),xtol=0.1,ftol=1)
    return n,f
    


