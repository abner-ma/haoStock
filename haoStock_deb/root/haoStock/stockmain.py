#-*- coding:utf-8 -*-
import urllib2
import math
from DateFile import *
from MYconfig import *
from MYsendmail import *

datefile_obj = DateFile('/root/mydeb/stock/')
outfile = datefile_obj.DateFileName()
MailTitle_str = "这是"+datefile_obj.GetFileName()+"股票情况"
MailTextMsg = "name代表股票名,turnover rate代表换手率,previous trading day close代表前一交易日收盘价,opening代表今日开盘价,price代表统计时的股价,StockCode代表股票代码"

output = open(outfile,"w")
finput = open('/root/stock/AllStockCode')

strStockCode = 's'
title = 'name'+','+'turnover rate'+','+'previous trading day close'+','+'opening'+','+'price'+','+'StockCode'+'\r'
output.write(title)
while True:
    line=finput.readline()
    if not line:
        break
    strStockCode = line
    url = 'http://qt.gtimg.cn/q='+strStockCode
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    response = resp.read()
    name = response.split('\"')[1].split('~')[1]
    price = response.split('\"')[1].split('~')[3]
    lastclose = response.split('\"')[1].split('~')[4]
    opening = response.split('\"')[1].split('~')[5]
    change=response.split('\"')[1].split('~')[38]
    stockStr = name+','+change+','+lastclose+','+opening+','+price+','+strStockCode
    output.write(stockStr)
finput.close()
output.close()

myconf = myconfig()
myconf.getConfig()
myobj = MYSendMail()
myobj.set_smtp_server(myconf.get_smtp_server(),25,myconf.get_user_name(),myconf.get_user_pw())
myobj.set_subject(MailTitle_str)
myobj.set_content(MailTextMsg)
myobj.set_mailfrom(myconf.get_user_name())
send_list = myconf.get_send_to()
myobj.add_mail_to(send_list[0])
myobj.add_attachment(outfile)
myobj.send_mail()
