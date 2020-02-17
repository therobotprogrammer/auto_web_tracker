#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:58:39 2019

@author: pt
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.headless = True
driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',options=chrome_options)

chrome_options.headless = False
driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',options=chrome_options)



driver.ChromeOptions.set_headless(True)
#chrome_options.add_argument("user-data-dir=chrome-data") 
driver.get('https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9')
time.sleep(3)  # Time to enter credentials

chrome_options.set_headless(False)
#chrome_options.add_argument("user-data-dir=chrome-data") 
driver.get('https://www.apple.com')
time.sleep(3)  # Time to enter credentials


chrome_options.set_headless(False)
#chrome_options.add_argument("user-data-dir=chrome-data") 
driver.get('https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9')
time.sleep(3)  # Time to enter credentials


##chrome_options.add_argument("user-data-dir=chrome-data") 
#driver.get('https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9')
#time.sleep(30)  # Time to enter credentials
#driver.quit()

#$ cat work.py 
#!/usr/bin/python3

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
driver = webdriver.Chrome('/home/pt/Documents/auto_web_tracker/chromedriver',options=chrome_options)
driver.get('https://www.amazon.com/gp/product/B07K3ZHM3V?pf_rd_p=183f5289-9dc0-416f-942e-e8f213ef368b&pf_rd_r=M0EHQ153B2FYH9CEGYZ9')  # Already authenticated
time.sleep(10)
driver.quit()


