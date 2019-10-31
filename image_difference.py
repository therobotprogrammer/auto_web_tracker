#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:00:31 2019

@author: pt
"""

#Credit for image diff code: https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/





# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import os


def blur(img_in, kernel_size = 3):
    img_out = cv2.GaussianBlur(img_in, (kernel_size,kernel_size),1,1)    
    return img_out

    



def get_diff_image(imageA_original, imageB_original):
    
    imageA = imageA_original.copy()
    imageB = imageB_original.copy()
    
    if imageA.shape != imageB.shape:
#        print('Shape Mismatch')
        return 'shape_mismatch'
    
    # load the two input images
#    imageA = cv2.imread(imageA_path)
#    imageB = cv2.imread(imageB_path)


    h = imageA.shape[0]
    w = imageB.shape[1]
    
    
    
    
    
    new_h_start = (int)(0*h)
    new_h_end = (int)(1*h)

    new_w_start = (int)(0*w)
    new_w_end = (int)(1*w)
    
    imageA = imageA[new_h_start:new_h_end, new_w_start:new_w_end]
    imageB = imageB[new_h_start:new_h_end, new_w_start:new_w_end]


#    loc = '/home/pt/Documents/ultimate_tracker/debug_images'
    loc = '/media/pt/ramdisk/debug_images'

    

    cv2.imwrite(loc + '/imageA.png', imageA)
    cv2.imwrite(loc + '/imageB.png', imageB)
    
        
 
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    
    grayA = blur(grayA, 19)
    grayB = blur(grayB, 19)    

    cv2.imwrite(loc + '/grayA.png', grayA)
    cv2.imwrite(loc + '/grayB.png', grayB)
    
    
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    cv2.imwrite(loc + '/diff.png', diff)
        
    
    
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
    	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    cv2.imwrite(loc + '/thresh.png', thresh)
    
    
    # loop over the contours
    for c in cnts:
    	# compute the bounding box of the contour and then draw the
    	# bounding box on both input images to represent where the two
    	# images differ
    	(x, y, w, h) = cv2.boundingRect(c)
    	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
     
    ## show the output images
    #cv2.imshow("Original", imageA)
    #cv2.imshow("Modified", imageB)
    #cv2.imshow("Diff", diff)
    #cv2.imshow("Thresh", thresh)
    
    
    
    
    # open the file with opencv
    if cv2.countNonZero(thresh) == 0 or score > .99 :
#        print("No change")    
        return None
        
    else:
#        cv2.imshow("Modified", imageB)
#        print("Change Detected")
        print("SSIM: {}".format(score))
        
        loc = '/media/pt/ramdisk/debug_images'
        
        if os.path.isdir(loc):            
            cv2.imwrite(loc + '/imageA.png', imageA)
            cv2.imwrite(loc + '/Modified.png', imageB)
            cv2.imwrite(loc + '/diff.png', diff)
            cv2.imwrite(loc + '/Thresh.png', thresh)

#        cv2.imshow("Original", imageA)
#        cv2.imshow("Modified", imageB)
#        cv2.imshow("Diff", diff)
#        cv2.imshow("Thresh", thresh)        
        

        return imageB
    

if __name__ == '__main__':   
    imageA_path = '/media/pt/ramdisk/auto_web_tracker/updated_baselines/walmart_<md5 HASH object @ 0x7f96bcc5a760>.png_3'
    imageB_path = '/media/pt/ramdisk/auto_web_tracker/updated_baselines/walmart_<md5 HASH object @ 0x7f96bcc5a760>.png_4'
    
    
    imageA = cv2.imread(imageA_path)
    imageB = cv2.imread(imageB_path)
    
    
    diff = get_diff_image(imageA, imageB) 
    
    if diff is not None:
#        cv2.imshow("Modified", diff)
        print("Change Detected")
#        cv2.waitKey(0)
    
    
    



































