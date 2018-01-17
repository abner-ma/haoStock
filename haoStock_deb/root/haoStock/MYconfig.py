#!/usr/bin/python
#-*-coding:UTF-8-*-

import ConfigParser

class myconfig(object):
    def __init__(self,configfile_name=None):
        if configfile_name == None:
            self.config_file_name = "/etc/haoStock/MYmail.ini"
        else:
            self.config_file_name = configfile_name
        self.send_to = []

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open(self.config_file_name, "rb"))
        self.smtp_server = config.get("global", "smtp_server")
        self.user_name = config.get("global", "user_name")
        self.user_pw = config.get("global", "user_pw")
        self.send_to = config.get("global", "send_to").split(',')

    def get_smtp_server(self):
        return self.smtp_server

    def get_user_name(self):
        return self.user_name
    
    def get_user_pw(self):
        return self.user_pw

    def get_send_to(self):
        return self.send_to
