#!/usr/bin/python
#-*-coding:UTF-8-*-

import datetime
import urllib2

today_str = datetime.datetime.now().strftime('%Y%m%d')

strStockCode = 'sz399001'
#strStockCode = 'sh000001'
url = 'http://qt.gtimg.cn/q='+strStockCode
req = urllib2.Request(url)
resp = urllib2.urlopen(req)
response = resp.read()
stockdate_str = response.split('\"')[1].split('~')[30]
print stockdate_str

if today_str == stockdate_str[0:8]:
	exit(0)
else:
	exit(1)
