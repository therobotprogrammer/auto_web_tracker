#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 18:08:07 2019

@author: pt
"""

import yagmail



class SendMail:
    def __init__(self, login_file = "/media/pt/hdd/login/yagmail.txt"):                
        f = open(login_file, "r")
        uname_password = str(f.read()).split(' ')
        uname = uname_password[0]
        password = uname_password[1]

        self.yag = yagmail.SMTP(uname, password)


    def send(self, to_email, subject = 'Tracker Update', body = 'Change Detected', attachment = None):
        
        
        
        #yag = yagmail.SMTP()
        if attachment is None:
            contents = [ body ]
        else:    
            contents = [ body, attachment ]
            
            
        self.yag.send(to_email, subject, contents)

        # Alternatively, with a simple one-liner:
        #yagmail.SMTP(uname).send(uname + '@gmail.com', 'subject', contents)
