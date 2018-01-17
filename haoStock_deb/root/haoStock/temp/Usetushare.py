#-*- coding:utf-8 -*-
import sys
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

class Usetushare:
    def __init__(self):
        reload(sys)
    def get_stock_basics(self):
        req_str="http://file.tushare.org/tsdata/all.csv"
        request = Request(req_str)
        text = urlopen(request, timeout=10).read()
        text = text.decode('GBK')
        text = text.replace('--', '')
        sys.setdefaultencoding('utf8')  
        output = open("txt","w")
        output.write(text)
        output.close()
        return 0

if __name__ == "__main__":
    Usetushare().get_stock_basics()

