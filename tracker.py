#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:24:44 2019

@author: pt
"""

import imgkit
import os
import cv2
import pandas as pd
import numpy as np

import sys
sys.path.insert(0, '/home/pt/Documents/auto_web_tracker')  
from image_difference import get_diff_image
from email_sender import SendMail
from UrlCapture import UrlCapture

import shutil
import hashlib 
import datetime
import time
import math

import tldextract
import pygame
from datetime import datetime

debug = False

image_format = '.png'




def add_if_new(new_img, img_list = []):
    change_detected_flag = False

    for im in img_list:   
        diff = get_diff_image(new_img, im)        
        if diff is None:            
            return change_detected_flag, img_list   

    #change detected    
    change_detected_flag = True
    img_list.append(new_img)
    
    return change_detected_flag, img_list



def print_to_dir(image_dict, output_dir): 
    if os.path.isdir(output_dir):
       shutil.rmtree(output_dir)
    os.makedirs(output_dir)
        
        
    for key in list(image_dict.keys()):        
        key_hash = hashlib.md5(key.encode()) 
        ext = tldextract.extract(key)
        domain = ext.domain
        
        filename = os.path.join(output_dir, domain + '_' + str(key_hash) + image_format)

        list_of_images = image_dict[key]
        
        count = 0
        for image in list_of_images:              
            cv2.imwrite(filename + '_' + str(count), image )
            count = count+1
            
    now = datetime.now()    
    current_time = now.strftime("%H:%M:%S")
    
    print('done printing to dict at ' + current_time)
    
    
    
def create_file_name(directory, url):
    ext = tldextract.extract(url)
    domain = ext.domain
    
    now = datetime.datetime.now()
    date_stamp = str(datetime.date.today())
    time_stamp = str(now.strftime("%H:%M:%S"))   

    date_timestamp = date_stamp + '__' + time_stamp   
    
    file_path = os.path.join(directory, domain + '__' + date_timestamp + image_format )

                        
    return file_path
    
    
    
   





work_dir = '/home/pt/Documents/auto_web_tracker'
scratch_dir = '/media/pt/ramdisk/auto_web_tracker'
changed_images_folder = os.path.join(work_dir, 'changed_images')
baseline_images_dir = os.path.join(work_dir, 'baseline_images')    



urls_df = pd.read_csv(os.path.join(work_dir , 'urls_to_track.csv'), usecols = ['url', 'description', 'window_width', 'window_height'])
#urls_df = pd.read_csv(os.path.join(work_dir , 'test.csv'), usecols = ['url', 'description', 'window_width', 'window_height'])

urls_df.set_index('url', drop = True, inplace=True)



def extract_domain(url):
    ext = tldextract.extract(url)
    domain = ext.domain  
    return domain

urls_df['domain'] = urls_df.index.map(extract_domain)



#domain resolution manual override




def get_one_url_per_domain(urls):
    domain_dict = {}
    
    for url in urls:
        ext = tldextract.extract(url)
        domain = ext.domain        
        domain_dict[domain] = url
        
    url_list_subset = []
    
    for domain in domain_dict:
        url_list_subset.append(domain_dict[domain])
        
    return url_list_subset






postman = SendMail()

if not debug:
    postman.send('trackerbot2020@gmail.com', subject = 'Test Mail from tracker', body = 'Test mail')


snapper = UrlCapture()

urls = list(urls_df.index)
urls_subset_for_cookies = get_one_url_per_domain(urls)


delay = 5
timeout_to_manually_activate_cookies = 1

snapper.set_cookies(urls_subset_for_cookies,  timeout = timeout_to_manually_activate_cookies)



for folder in [work_dir, scratch_dir, changed_images_folder, baseline_images_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)            
 

baseline_image_dict = {}



temp_file = os.path.join(scratch_dir, 'temp' + image_format)

if debug:
    max_variations = 3
else:
    max_variations = 10
    


snapper.headless = True


print('Adding variations')

for variation in range(0, max_variations):
    for url, row in urls_df.iterrows():        
        if os.path.exists(temp_file):
          os.remove(temp_file)        
#        print(url)
#        imgkit.from_url(url, temp_file)        
        w = row['window_width']
        h = row['window_height']        
        
        
        if math.isnan(w)   or  math.isnan(h)  :
            snapper.capture(url, temp_file, delay = delay)
        else:
            snapper.capture(url, temp_file, window_size = (int(w) ,int(h)), delay = delay)
            

            
        
        img = cv2.imread(temp_file)        
        
        if url in baseline_image_dict.keys():
            change_detected_flag, baseline_image_dict[url] = add_if_new(img, baseline_image_dict[url])
        else:
            change_detected_flag, baseline_image_dict[url] = add_if_new(img, [])
            
        
#        print('>>' , len(baseline_image_dict[url]))
        if change_detected_flag:
            print('Baseline variation detected in URL >>> ' , url)
        
    print(variation)
    
    if debug:
        continue
    else:
        time.sleep(1)





print_to_dir(baseline_image_dict, baseline_images_dir)



print('started while loop')

while(1):
    temp_file = os.path.join(scratch_dir, 'temp' + image_format)

    for url, row in urls_df.iterrows():        
        if os.path.exists(temp_file):
          os.remove(temp_file)
          
        try:
#            imgkit.from_url(url, temp_file)
            w = row['window_width']
            h = row['window_height']
            
            if math.isnan(w)   or  math.isnan(h)  :
                snapper.capture(url, temp_file, delay = delay)
            else:
                snapper.capture(url, temp_file, window_size = (int(w) ,int(h)), delay = delay)
                

                

        except:
            continue
        
#        time.sleep(5)
        
        new_img = cv2.imread(temp_file)     
        
        baseline_images_for_url = baseline_image_dict[url]
        
        found_in_archive = False
        
        for baseline in baseline_images_for_url:
#            loc = os.path.join(scratch_dir, 'debug_images')
#        
#            cv2.imwrite(loc + '/new_img' + image_format, new_img)
#            cv2.imwrite(loc + '/baseline' + image_format, baseline)
            
            diff = get_diff_image(new_img, baseline)
            if diff is None:
                #image found in archive
                found_in_archive = True
                break
            
            
        if not found_in_archive:
                change_detected_flag, baseline_images_for_url = add_if_new(new_img, baseline_images_for_url)
                
                if change_detected_flag:
                    print('New Shape added >>> ', url)
    
                    filename = create_file_name(changed_images_folder, url)  
                    
                    if type(diff) is not str:
                        pygame.mixer.init()
                        pygame.mixer.music.load("ringtone.mp3")
                        pygame.mixer.music.play(-1)
                        
                        
                        cv2.imwrite(filename, diff)
    
                        ext = tldextract.extract(url)
                        domain = ext.domain
                        postman.send('trackerbot2020@gmail.com', subject = 'Change > ' + domain, attachment = filename )
                    
                    
                else:
                    print('Shape Found in archive')
                    break
             
    updated_baselines_dir =  os.path.join(scratch_dir, 'updated_baselines')
    if os.path.isdir(updated_baselines_dir):
        shutil.rmtree(updated_baselines_dir)
        
    os.makedirs(updated_baselines_dir)
    print_to_dir(baseline_image_dict, os.path.join(scratch_dir, 'updated_baselines') )

    if debug :  
        continue
    else:
        time.sleep(60)                
        









snapper.turn_off_driver()















