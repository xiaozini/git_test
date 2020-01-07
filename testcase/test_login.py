from common.readExcel import ReadExcel
import os
import unittest,requests
import yaml
from ddt import ddt,data
from common.readRequests import SendRequests

path = os.path.join(os.path.dirname(os.getcwd()),'resource','test_api2.xlsx')
testcast = ReadExcel.readExcel(path,'login')

#获取根目录
ypath = os.path.join(os.path.dirname(os.getcwd()),'common','token.yaml')
print('根目录为:%s'%ypath)

@ddt
class DdtTest(unittest.TestCase):
    def setUp(self):
        self.s = requests.session()
    def tearDown(self):
        pass

    @data(*testcast)
    def test_api(self,data):
        re = SendRequests().sendRequests(self.s,data)
        true_status = int(re['status'])

        if true_status == 1:
            #获取token 并放在yaml上
            login_token = re['data']['token']
            print('login_token:%s'%login_token)
            with open(ypath,'w',encoding='utf-8') as f:
                yaml.dump(login_token,f)

        print('ddt中数据为:%s'%re)
        expect_result = data['expect_result'].split(':')[1]
        self.assertEqual(true_status,int(expect_result),'实际返回数据为:%s'%re)


if __name__ == '__main__':
    unittest.main()