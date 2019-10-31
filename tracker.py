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

image_format = '.png'


delay = 3


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
        
    print('done')
    
    
    
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




#urls = [    'https://www.apple.com/'    ]

#url_itemname_dict = {               
#            'https://www.bestbuy.com/site/apple-refurbished-12-9-inch-ipad-pro-256gb-silver/5665301.p?skuId=5665301' : 'iPad (Refurb) 256GB',            
#            'https://www.bestbuy.com/site/apple-ipad-pro-12-9-inch-2nd-generation-with-wi-fi-cellular-512-gb-silver/5505700.p?skuId=5505700' : '2017 iPad 512GB Silver - BestBuy',
#            'https://www.bestbuy.com/site/apple-ipad-pro-12-9-inch-2nd-generation-with-wi-fi-cellular-512-gb-gold/5505701.p?skuId=5505701': '2017 iPad 512GB Silver - BestBuy',
#            
#            
#            'https://www.bestbuy.com/site/apple-ipad-pro-12-9-inch-2nd-generation-with-wi-fi-cellular-256-gb-space-gray/9079049.p?skuId=9079049': 'iPad 256 Gray - Bestbuy',
#            'https://www.bestbuy.com/site/apple-ipad-pro-12-9-inch-2nd-generation-with-wi-fi-cellular-256-gb-silver/5502100.p?skuId=5502100': 'iPad 256 Silver - BestBuy',
#            'https://www.bestbuy.com/site/apple-12-9-inch-ipad-pro-latest-model-with-wi-fi-cellular-512gb-space-gray/4905101.p?skuId=4905101': 'iPad 512 Silver - BestBuy',
#            'https://www.bestbuy.com/site/apple-12-9-inch-ipad-pro-latest-model-with-wi-fi-cellular-512gb-silver/4905500.p?skuId=4905500': 'iPad 512 Gray - BestBuy',
#            'https://www.bestbuy.com/site/apple-12-9-inch-ipad-pro-latest-model-with-wi-fi-cellular-1tb-space-gray/4905600.p?skuId=4905600' : 'iPad 1TB - BestBuy',
#            'https://www.bestbuy.com/site/apple-12-9-inch-ipad-pro-latest-model-with-wi-fi-cellular-1tb-silver/4905700.p?skuId=4905700': 'iPad 1TB - BestBuy',
#
#
#            'https://www.amazon.com/dp/B07K3ZHM3V/ref=cm_sw_r_tw_dp_U_x_yJvUDb5BG19RV?th=1' : 'iPad 256 Gray - Amazon',
#            'https://www.amazon.com/dp/B07K3ZM47N/ref=cm_sw_r_tw_dp_U_x_yJvUDb5BG19RV?th=1' : 'iPad 256 Silver - Amazon',
#            'https://www.amazon.com/dp/B07K3B4NBH/ref=cm_sw_r_tw_dp_U_x_yJvUDb5BG19RV' : 'iPad 512 Gray - Amazon',
#            'https://www.amazon.com/dp/B07K438MJV/ref=cm_sw_r_tw_dp_U_x_FKvUDbBW115H9 ' : 'iPad 512 Silver - Amazon',
#            'https://www.amazon.com/dp/B07K344LR9/ref=cm_sw_r_tw_dp_U_x_BZvUDbV7ASB1K' : 'iPad 1TB Gray - Amazon',
#            'https://www.amazon.com/dp/B07K3BZSN3/ref=cm_sw_r_tw_dp_U_x_Q0vUDb4R8A95BK' : 'iPad 1TB Silver - Amazon',
#            
#            
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-Wi-Fi-Cellular-256GB-Silver/356659182?selected=true' : 'iPad 256 Silver ',
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-Wi-Fi-Cellular-256GB/507838389?selected=true' : 'iPad 256 Gray',
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-Wi-Fi-Cellular-512GB-Silver/174902580?selected=true' : 'iPad 512 Silver',
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-Wi-Fi-Cellular-512GB/221098689?selected=true' : 'iPad 512 Black',
#            
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-1TB-WiFi-Cellular-Silver/688634941?selected=true' : 'iPad 1Tb Silver',
#            'https://www.walmart.com/ip/Apple-12-9-inch-iPad-Pro-2018-1TB-WiFi-Cellular/965075552?selected=true' : 'iPad 1Tb Gray',
#            
#            'https://www.bhphotovideo.com/c/product/1441852-REG/apple_mtj02ll_a_12_9_ipad_pro_late.html': 'iPad',
#            'https://www.bhphotovideo.com/c/product/1441853-REG/apple_mtja2ll_a_12_9_ipad_pro_late.html': 'iPad',
#            'https://www.bhphotovideo.com/c/product/1441855-REG/apple_mtjn2ll_a_12_9_ipad_pro_late.html': 'iPad',
#            'https://www.bhphotovideo.com/c/product/1441854-REG/apple_mtjh2ll_a_12_9_ipad_pro_late.html': 'iPad',
#            'https://www.bhphotovideo.com/c/product/1441856-REG/apple_mtju2ll_a_12_9_ipad_pro_late.html': 'iPad',
#            'https://www.bhphotovideo.com/c/product/1441857-REG/apple_mtl02ll_a_12_9_ipad_pro_late.html': 'iPad',   
#            'https://www.bhphotovideo.com/c/product/1342553-REG/apple_mpll2ll_a_12_9_ipad_pro_mid.html' : 'iPad 2017 - B&H'
#
#        }
#
#urls_df = pd.DataFrame.from_dict(url_itemname_dict,  orient = 'index', columns = ['description'])
#urls_df.to_csv(os.path.join(work_dir , 'urls_to_track.csv') )


#urls_df = pd.read_csv(os.path.join(work_dir , 'urls_to_track.csv'), usecols = ['url', 'description', 'window_width', 'window_height'])
urls_df = pd.read_csv(os.path.join(work_dir , 'test.csv'), usecols = ['url', 'description', 'window_width', 'window_height'])

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
snapper = UrlCapture()

urls = list(urls_df.index)
urls_subset_for_cookies = get_one_url_per_domain(urls)

snapper.set_cookies(urls_subset_for_cookies,  timeout = 30)





for folder in [work_dir, scratch_dir, changed_images_folder, baseline_images_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)            
 

baseline_image_dict = {}



temp_file = os.path.join(scratch_dir, 'temp' + image_format)

max_variations = 1



snapper.headless = True


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
        
    time.sleep(5)





print_to_dir(baseline_image_dict, baseline_images_dir)



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
                snapper.capture(url, temp_file, window_size = (int(w) ,int(h)), dalay = delay)
                

                

        except:
            continue
        
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

    time.sleep(60)                
        









snapper.turn_off_driver()















