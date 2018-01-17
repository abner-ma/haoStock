#!/usr/bin/python
#-*-coding:UTF-8-*-

import datetime

class DateFile(object):
    filePath = ''
    fileName = ''
    fileType = ''
    def __init__(self, filePath = './',fileType = '.csv'):
        self.filePath = filePath
        self.fileType = fileType
        self.fileName = datetime.datetime.now().strftime('%Y%m%d')

    def DateFileName(self):
        return self.filePath + self.fileName + self.fileType

    def GetFileName(self):
        return self.fileName


#print DateFile('/root/').DateFileName()
#print file name.('path/yyyymmdd.xxx)        

