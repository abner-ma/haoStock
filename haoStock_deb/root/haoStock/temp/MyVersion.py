#-*- coding:utf-8 -*-

class MyVersion():
    version_file_fd=''
    def __init__(self):
		self.version_file_fd = open("./VERSION","r")

    def showVersion(self):
        ver=self.version_file_fd.readline()
        self.version_file_fd.close()
        return ver


if __name__ == '__main__':
    myV_obj = MyVersion()
    print myV_obj.showVersion()
