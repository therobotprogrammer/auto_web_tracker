#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:24:26 2019

@author: pt
"""

from selenium import webdriver
import pandas as pd
import time
import os
import shutil 
import pickle
import tldextract
import cv2


class UrlCapture:
    def __init__(self, delete_previous_cookies = False, window_size = (1920,1080), headless = True, cut_borders = False):
        self.cookies_dir = os.path.join( os.getcwd() , 'cookies')
        self.cookies_pkl_file = os.path.join( os.getcwd() , 'cookies_pkl')


        if delete_previous_cookies and os.path.isdir(self.cookies_dir):
            shutil.rmtree(self.cookies_dir)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--user-data-dir=" + self.cookies_dir)

        self.default_window_size = window_size
        self.current_window_size = None
        
        self.headless = headless

        self.cut_borders = cut_borders
        
#        self.driver = None


    def set_cookies(self, urls, timeout = 40):
        print('>>>>> Setting Cookies <<<<<')
        options = self.options
        options.headless = False
        
        local_driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',   options=options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])  # Optional argument, if not specified will search path.
        local_driver.set_window_size(self.default_window_size[0],self.default_window_size[1])      #the trick

        for url in urls:          
            local_driver.get(url)
            time.sleep(timeout)  # Time to enter credentials
            
        pickle.dump( local_driver.get_cookies() , open(self.cookies_pkl_file,"wb"))

        local_driver.quit()
        
        print('>>>>> Finished Setting Cookies <<<<<')


        
    def capture(self, url, location, window_size = 'default', delay = 0):
        
        if os.path.isdir(self.cookies_dir):
            shutil.rmtree(self.cookies_dir, ignore_errors=True)
        
        
        headless = self.headless
        
        self.options.headless = headless            
        driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',   options=self.options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])  # Optional argument, if not specified will search path.


        if window_size == 'default':                
            driver.set_window_size(self.default_window_size[0],self.default_window_size[1])      #the trick
            self.current_window_size = self.default_window_size

        else:
            driver.set_window_size(window_size[0],window_size[1])      #the trick
            self.current_window_size = window_size              

#        print()
#        print('>>>>> Ready to Capture <<<<<')
   



        ext = tldextract.extract(url)
        domain = ext.domain
        
#        driver.get(domain)
        
        
        



        cookies = pickle.load(open(self.cookies_pkl_file, "rb"))
        for cookie in cookies:
#            print(cookie)
            if domain in  cookie['domain']:
                #visit url before adding cookie of the url
#                driver.get(domain_in_cookie)
                driver.get(url)
                
                if 'expiry' in cookie:
                    del cookie['expiry']
                driver.add_cookie(cookie)

        driver.get(url)
        time.sleep(delay)
        driver.save_screenshot(location)
        

        
    

        
        # Cut borders

        if self.cut_borders:
        # tod do: clean this

            imageA = cv2.imread(location)
            
            h = imageA.shape[0]
            w = imageA.shape[1]
            new_h_start = (int)(.25*h)
            new_h_end = (int)(1*h)        
            new_w_start = (int)(0*w)
            new_w_end = (int)(.9*w)
            
            imageA = imageA[new_h_start:new_h_end, new_w_start:new_w_end]

            cv2.imwrite(location, imageA)


        driver.quit()
        driver = None

#        print('Captured:  ' , url)



if __name__ == '__main__':
    snapper = UrlCapture(window_size = (1920,1080), headless = False)
    
    urls = ['https://www.cowin.gov.in/']
    snapper.set_cookies(urls, timeout = 3)
    
    w = 1920
    h= 1080
    
    snapper.capture(urls[0], 'test.png', window_size = (w,h), delay = 3)

    
#    snapper.capture('https://www.cowin.gov.in/', 'test.png')
    
#    time.sleep(3)  # Time to enter credentials


#driver.get('http://www.google.com/');
#time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
#driver.quit()
#


#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=selenium") 
#driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver', options=options)
#driver.get("www.google.com")

#
#
#total_height = 1080
#driver.set_window_size(1920, total_height)      #the trick
#
#driver.get('https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9')
#el = driver.find_element_by_tag_name('body')
#el.screenshot('screenshot_body.png')
#
#driver.save_screenshot("screenshot1.png")
#
#driver.get('https://www.apple.com/shop/refurbished/ipad/wi-fi-cellular-ipad-pro-12-9')
#driver.save_screenshot("screenshot2.png")

#time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ipad 12.9 inch')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
#driver.quit()
#

