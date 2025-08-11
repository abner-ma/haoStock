#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import getopt
import urllib.request

myparams={'-h/--help         print usage for this script.',
        '-o [filename]      output to file'}

def parseparams(opts):
    for opt,arg in opts:
        if opt in ("-h","--help"):
            showhelp()
        elif opt in ("-o"):
            outfile=arg
            writetofile(outfile)

def writetofile(outfile):
    output = open(outfile,"w")
    finput = open('AllStockCode')

    strStockCode = 's'
    title = 'name,turnover rate,previous trading day close,opening,price,StockCode \r'
    output.write(title)
    while True:
        line=finput.readline()
        if not line:
            break
        strStockCode = line
        url = 'http://qt.gtimg.cn/q='+strStockCode
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        response = resp.read()
        parts = response.split(str.encode('\"'))
        if len(parts) > 1:
            subparts = parts[1].split(str.encode('~'))
            if len(subparts) > 38:
                name = subparts[1]
                price = subparts[3]
                lastclose = subparts[4]
                opening = subparts[5]
                change= subparts[38]
            # else:
            #     print("Error: '~' not found in the response.")
        # else:
        #     print("Error: '\"' not found in the response.")
        # name = response.split(str.encode('\"'))[1].split(str.encode('~'))[1]
        # price = response.split(str.encode('\"'))[1].split(str.encode('~'))[3]
        # lastclose = response.split(str.encode('\"'))[1].split(str.encode('~'))[4]
        # opening = response.split(str.encode('\"'))[1].split(str.encode('~'))[5]
        # change=response.split(str.encode('\"'))[1].split(str.encode('~'))[38]
        stockStr = name.decode('GBK')+','+change.decode()+','+lastclose.decode()+','+opening.decode()+','+price.decode()+','+strStockCode
        output.write(stockStr)
        #print(response.decode('hex'))
    finput.close()
    output.close()

def showhelp():
    it = iter(myparams)
    for x in it:
        print(x,end=" ")
        print('\r')

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:", ["help"])
        except (getopt.error,msg):
            raise Usage(msg)
        parseparams(opts)
    except (Usage, err):
        pass
        # print >>sys.stderr, err.msg
        # print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
