#coding=utf-8
import os
import codecs
import configparser

#绝对路径
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir,'config.ini')

class ReadConfig:


    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self,name):
        value = self.cf.get("EMAIL",name)
        return value

    def get_http(self,name):
        value = self.cf.get("HTTP",name)
        return value


    def get_url(self,name):
        value = self.cf.get("URL",name)
        return value

    def get_db(self,name):
        value = self.cf.get("DATABASE",name)
        return value

#
# if __name__ == "__main__":
#     config = ReadConfig()
#     baseurl = config.get_http('baseurl')
#     print(baseurl)