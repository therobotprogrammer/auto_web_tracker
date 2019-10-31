#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#==========================================# 
# Author: Pranav
# If you find this code useful, 
# please include this section and give 
# credit to original author.  
#==========================================
"""

import os, sys
import zipfile
import wget
import shutil
import requests
import datetime
import pandas as pd
import pytz
from pytz import timezone
import time
from glob import glob


last_download_speed = 0 
last_download_percentages = ''

### Pushover Login Credentials
pushover_user_key = ''
pushover_token = ''

last_message_time = -1
flag_first_hour_message_sent = False
options = {}


class AutoDownloader(object):  
  
    def __init__(self, local_timezone =  'Asia/Kolkata'):
        self.last_message_time = -1
        self.flag_first_hour_message_sent = False
        self.local_timezone = local_timezone

        
    def initiate(self, project_dir, data_to_download, common_utils_dir = 'default', recreate_dir = True):           
        if not os.path.isdir(project_dir):
            os.makedirs(project_dir)
        elif recreate_dir == True:
            shutil.rmtree(project_dir)
            os.makedirs(project_dir)
            
        os.chdir(project_dir)
        print('>>>>>Confirm Project Directory: ' + project_dir)
        sys.path.insert(0, project_dir)           
        
        if common_utils_dir == 'default':
            common_utils_dir = project_dir + '/COMMON_UTILS'
    
        self.__download_common_utils(common_utils_dir)        
        from pyaria2 import PyAria2 ###############################################################???
           
        downloader = PyAria2()
        time.sleep(1)    

        self.__add_files_to_aria(downloader, project_dir, data_to_download, common_utils_dir)                
        self.__printDownloadStatus(downloader)        

        print('\n>>>Unzipping') 
        self.__unzip_all(project_dir, data_to_download)        
        
        #self.showDirectory(project_dir)
        
        self.all_gids = []
        del downloader

    def recursively_add_to_path(self, currentDir):
        print('Warning: Only add code to path that you know is safe. Recusrively adding code is not recommended')
        print('Ignoring files ending with __ or that have a . ')
        
        index = 0
        
        sys.path.insert(0, currentDir)
        print('Added to path: ' + currentDir)
        
        for root, dirs, files in os.walk(currentDir):
          for dir in dirs:
              newDir = os.path.join(root, dir)
              index += 1
              if not (newDir.endswith('__') or len(newDir.split('.')) > 1 ):
                  print('Added to path: ' + newDir)
                  sys.path.insert(0, newDir)           

        
    def __download_common_utils(self, common_utils_dir):
        if os.path.isdir(common_utils_dir):
            shutil.rmtree(common_utils_dir)
           
        os.makedirs(common_utils_dir)
    
        aria_url = 'https://raw.githubusercontent.com/zhenlohuang/pyaria2/master/pyaria2.py'
        wget.download(aria_url , common_utils_dir)
        
        kaggle_api_url = 'https://github.com/thegreatskywalker/kaggle-api/archive/master.zip'
        wget.download(kaggle_api_url , common_utils_dir)
        self.unzip_individual_directory(common_utils_dir)  
        os.rename(common_utils_dir + '/kaggle-api-master' , common_utils_dir + '/__kaggle-api-master__')
        sys.path.insert(0, common_utils_dir + '/__kaggle-api-master__/kaggle') 
        sys.path.insert(0, common_utils_dir + '/__kaggle-api-master__/kaggle/api') 
        sys.path.insert(0, common_utils_dir + '/__kaggle-api-master__/kaggle/models') 

        #sys.path.insert(0, common_utils_dir) 
        print('\n\n')
        sys.path.insert(0, common_utils_dir)           
        
        
        
        ###############################################################
    def __download_url(self, downloader,directory, url):    
        os.chdir(directory)
        global_download_options = downloader.getGlobalOption()
        global_download_options['max-connection-per-server'] = '16'
        downloader.changeGlobalOption(global_download_options)
        gid=downloader.addUri([url], {'dir':directory})
        self.all_gids.append(gid)


   
    def __unzip_all(self, project_dir, data_to_download):
        for directory, url_links in data_to_download.items():        
            full_path_directory = project_dir + directory
            self.unzip_individual_directory(full_path_directory)
    
    
    
    def unzip_individual_directory(self, full_path_directory):    
        print('\nUnzipping items in '+ full_path_directory)
        extension = ".zip"
    
        for item in os.listdir(full_path_directory):            
            if item.endswith(extension): # check for ".zip" extension
                file_name = full_path_directory + '/' + item # get full path of files
                
                print('Unzipping: '+file_name)
                zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                zip_ref.extractall(full_path_directory) # extract file to dir
                zip_ref.close() # close file
                os.remove(file_name) # delete zipped file



    ################################################
    def __printDownloadStatus(self, downloader):
        
        #Print list of all files to be downloaded
        print('\n\n>>>Downloads Started\n')
        
        for item in self.all_gids:        
            status = downloader.tellStatus(item)
            temp = status['files'][0]
            temp = temp['uris']
            temp = temp[0]
            url = temp['uri']    
            print('['+ str(self.all_gids.index(item)) + ']' + url)
        print('\n')
        while downloader.tellActive(): 
            self.__print_status(downloader)
        
        self.__print_status(downloader, False) #Because previous loop will show 98% complete and then terminate at 100%. 
        message = '  Speed: ' + str(self.last_download_speed) + 'MBps  ' 
        sys.stdout.write(message)
#        time.sleep(.3)  
#        sys.stdout.flush()
        
        print('\nDownloading Complete \n\n')
        downloader.shutdown() 
 
    def __print_status(self, downloader, print_speed = True):
        message = ''
        total_speed = 0
        for item in self.all_gids:        
            status = downloader.tellStatus(item)
            
            
            #if status['status'] == 'active':              
            completedLength = float(status['completedLength'])
            totalLength = float(status['totalLength'])
            
            if not totalLength == 0:                
                percentage_completed = (completedLength / totalLength) * 100
                percentage_completed = int(percentage_completed)
                #percentage_completed = round(percentage_completed, 0) 
            else:
                message = '?'
                percentage_completed = completedLength
                percentage_completed = int(percentage_completed)

                #percentage_completed = completedLength
                            
            speed = int(status['downloadSpeed']) /(1024*1024) 
            speed = round(speed, 2)              
            total_speed+= speed
            message+= '['+ str(self.all_gids.index(item)) + ']'+ str(percentage_completed) + '% '
        
        if print_speed == True: 
            self.last_download_percentages = message
            self.last_download_speed = total_speed
            message += '  Speed: ' + str(total_speed) + 'MBps  ' 
            sys.stdout.write('\r'+ message)
            time.sleep(.3)  
            sys.stdout.flush() 
        else:
            sys.stdout.write('\r'+ message)
        
        

    def __add_files_to_aria(self, downloader, project_dir, data_to_download, common_utils_dir):  
        self.all_gids = []
           
        print('>>>Creating Directory Structure: \n')
        for directory, url_links in data_to_download.items():
            full_path_directory = project_dir + directory            
            if os.path.isdir(full_path_directory) and (full_path_directory != common_utils_dir):
                print('Data previously downloaded at: ' + full_path_directory)
            else:
                if(full_path_directory != common_utils_dir):
                    print('Creating directory: '+ full_path_directory )                    
                    os.makedirs(full_path_directory)
                    
                for url in url_links:
                    if self.url_check_syntax_only(url):
                        self.__download_url(downloader,full_path_directory, url) 
                    else:
                        self.download_kaggle_project(full_path_directory, url)


    def download_kaggle_project(self, directory, competition):
        from kaggle_api_extended import KaggleApi
        
        kaggle = KaggleApi()
        kaggle.authenticate()       
        kaggle.competition_download_files(competition, path = directory)
        
        
 
    def url_check_online(self,url):    
        r = requests.head(url)
        if r.status_code < 400:
            return True
        else:
            return False
        
        
     
    def url_check_syntax_only(self,url): 
       if '://' in url:
           return True
       else:
           return False


    def showDirectory(self, path,show_files=True, indentation=2,file_output=False):
        """
        Shows the content of a folder in a tree structure.
        path -(string)- path of the root folder we want to show.
        show_files -(boolean)-  Whether or not we want to see files listed.
                                Defaults to False.
        indentation -(int)- Indentation we want to use, defaults to 2.   
        file_output -(string)-  Path (including the name) of the file where we want
                                to save the tree.
        """
        print('>>>Directory Tree at' + path + '\n\n')
        tree = []
        
        if not show_files:        
            for root, dirs, files in os.walk(path):
                if not '__' in root:
                    level = root.replace(path, '').count(os.sep)
                    indent = ' '*indentation*(level)
                    #tree.append('{}{}/'.format(indent,os.path.basename(root)))
                    if file_output:
                        tree.append('{}{}/'.format(indent,os.path.basename(root)))   
                    else:
                        tree.append('{}{}'.format(indent,'['+ os.path.basename(root) + ']'))    
        
        if show_files:
            for root, dirs, files in os.walk(path):  
                if not '__' in root:
                    level = root.replace(path, '').count(os.sep)
                    indent = ' '*indentation*(level)
                    
                    if file_output:
                        tree.append('{}{}/'.format(indent,os.path.basename(root)))   
                    else:
                        tree.append('{}{}'.format(indent,'['+ os.path.basename(root) + ']'))    

                    for f in files:
                        subindent=' ' * indentation * (level+1)
                        tree.append('{}{}'.format(subindent,f))                            

        
        if file_output:
            os.chdir(path)
            output_file = open(file_output,'w')
            for line in tree:
                output_file.write(line)
                output_file.write('\n')
        else:
            # Default behaviour: print on screen.
            for line in tree:
                print (line)
                

    def setup_pushover_credintials(self,user_key, token):
        self.pushover_user_key = user_key
        self.pushover_token = token
        

    def send_notification(self,msg_string):
        
        ''' 
            Credit for function: binga Phani Srikanth
            http://forums.fast.ai/t/training-metrics-as-notifications-on-mobile-using-callbacks/17330
        
            This function sends message to my mobile using Pushover.
        '''          
        
        url = "https://api.pushover.net/1/messages.json"
        data = {
            'user'  : self.pushover_user_key,
            'token' : self.pushover_token,
            'sound' : "gamelan"
        }
        data['message'] = msg_string
        #data['message'] = data['message'] + "\n" + str(datetime.now())
    
        r = requests.post(url = url, data = data)
        



    def send_notification_every_x_minutes(self,msg_string, time_interval_minutes = 60):
        if time_interval_minutes == 0:
           self.send_notification(msg_string)
           return True
        
        current_time = datetime.datetime.now() 
        
        if self.last_message_time == -1:
            self.send_notification(msg_string)
            self.last_message_time = current_time  

        else:
            time_difference = current_time - self.last_message_time
            time_different_minutes = time_difference.total_seconds() / 60

            if time_different_minutes >= time_interval_minutes:
               self.send_notification(msg_string)
               self.last_message_time = current_time   
               return True
        return False
        
        
    def send_notification_clock_multiples(self,msg_string, time_interval = 1, minute_interval = True): 
        #US timezone: 'US/Eastern'               
        
        if time_interval == 0:
           time_interval = 1 # avoids division by 0 

        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone(pytz.timezone(self.local_timezone))

        
        if self.last_message_time == -1:
            self.send_notification(msg_string)
            self.last_message_time = local_time
            return True            
        
        else:
            time_difference = local_time - self.last_message_time 
            if minute_interval == True:
                time_difference = time_difference.total_seconds() / 60
            else:
                time_difference = time_difference.total_seconds() / (60*60) #hourly

            if minute_interval == True:
                if time_difference >= time_interval:    
                       if local_time.minute == 0:                   
                           self.send_notification(msg_string)
                           self.last_message_time = local_time 
                           return True
                       elif local_time.minute % time_interval == 0:
                           self.send_notification(msg_string)
                           self.last_message_time = local_time  
                           return True
                       
            if minute_interval == False:  
               if self.flag_first_hour_message_sent == False:
                   if local_time.hour % 1 == 0 and local_time.minute == 0: 
                     self.send_notification(msg_string)
                     self.last_message_time = local_time
                     self.flag_first_hour_message_sent = True
                     return True

               elif time_difference >= time_interval:                     
                   if local_time.hour % time_interval == 0:
                       self.send_notification(msg_string)
                       self.last_message_time = local_time 
                       return True
        return False
        
        
        
        
    def get_time_string(self):
        
        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone(pytz.timezone(self.local_timezone))  
                
        year = str(local_time.year)  
        month = str(local_time.month) 
        day = str(local_time.day) 
        hour = str(local_time.hour)
        minute = str(local_time.minute)
        
        time_string = year + '-' + month + '-' + day + '-' + hour + '-' + minute
        return(time_string)
                
        
        
        
        
        
        
        
        
        
        


