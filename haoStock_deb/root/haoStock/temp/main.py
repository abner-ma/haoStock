#-*- coding:utf-8 -*-

"""
This is main
"""
import os
import sys
import getopt

from MyVersion import *

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
		
    try:
        try:
            opts,argv = getopt.getopt(argv[1:],"hwv",["help","weixin","version"])
        except getopt.error,msg:
            raise Usage(msg)
        #more code
        for name,value in opts:
            if name in ('-w','--weixin'):
                os.system("python  weixinrebot.py")
            if name in ('-h','--help'):
                print "need help"
            if name in ('--version','-v'):
                print MyVersion().showVersion()
	
    except Usage,err:
        print >>sys.stderr,err.msg
        print >>sys.stderr,"for help use --help"
        return 2

    print "end."

if __name__ == "__main__":
    sys.exit(main())
