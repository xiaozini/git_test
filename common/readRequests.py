import urllib3
import json

class SendRequests():

    def sendRequests(self,s,apiData):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = apiData['url']
        method = apiData['method']
        header = apiData['header']
        body = apiData['body']
        if "token" in body:
            #替换Token值
            pass


        res = s.request(url = url,json = json.loads(body),headers=json.loads(header),method = method,verify=False)
        resultJson = res.json()
        print('返回数据为111:%s' % resultJson)
        return resultJson