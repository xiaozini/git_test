#coding=utf-8
import requests
import readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()
class ConfigHttp:

    def __init__(self):
        global host,port,timeout
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http('port')
        timeout = localReadConfig.get_http('timeout')
        self.Log = Log.get_log()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}

    def set_url(self,url):
        self.url = host+url

    def set_headers(self,header):
        self.headers = header
    def set_data(self,data):
        self.data = data

    def set_params(self,params):
        self.params = params

    def set_files(self,file):
        self.files = file

    def get(self):
        try:
            response = requests.get(self.url,params=self.params,headers=self.headers,timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    def post(self):
        try:
            response = requests.get(self.url, data=self.data, headers=self.headers, files = self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

if __name__ == '__main__':
    c = ConfigHttp()
    print(c.set_url())