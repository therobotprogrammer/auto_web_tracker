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


class UrlCapture:
    def __init__(self, delete_previous_cookies = False, window_size = (1920,1080)):
        self.cookies_dir = os.path.join( os.getcwd() , 'cookies')

        if delete_previous_cookies and os.path.isdir(self.cookies_dir):
            shutil.rmtree(self.cookies_dir)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--user-data-dir=" + self.cookies_dir)
        self.window_size = window_size

        self.driver = None


    def set_cookies(self, urls, timeout = 3):
        print('>>>>> Setting Cookies <<<<<')
        options = self.options
        options.headless = False

        local_driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',   options=options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])  # Optional argument, if not specified will search path.

        for url in urls:          
            local_driver.get(url)
            time.sleep(timeout)  # Time to enter credentials
            
        local_driver.quit()
        
        print('>>>>> Finished Setting Cookies <<<<<')

        
    def capture(self, url, location, headless = False):
        if self.driver is None:            
            self.options.headless = headless            
            self.driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',   options=self.options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])  # Optional argument, if not specified will search path.

            self.driver.set_window_size(1920,1080)      #the trick
            
            print()
            print('>>>>> Ready to Capture <<<<<')


        self.driver.get(url)
        self.driver.save_screenshot(location)
        
        
        
        print('Captured:  ' , url)


    def turn_off_driver(self):
        self.driver.quit()
        

if __name__ == '__main__':
    snapper = UrlCapture()
    
    urls = ['https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9']
    snapper.set_cookies(urls)
    
    snapper.capture('https://www.apple.com/', 'test.png')
    
    time.sleep(10)  # Time to enter credentials
    snapper.turn_off_driver()


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

