from common.readExcel import ReadExcel
import os
import unittest,requests
from common.read_token import get_token
from ddt import ddt,data
from common.readRequests import SendRequests

path = os.path.join(os.path.dirname(os.getcwd()),'resource','test_api2.xlsx')
testcast = ReadExcel.readExcel(path,'userinfo')

@ddt
class TestUserInfo(unittest.TestCase):
    def setUp(self):
        self.s = requests.session()
    def tearDown(self):
        pass

    @data(*testcast)
    def test_api(self,data):
        expect_result = data['expect_result'].split(':')[1]
        # 获取token 并放在yaml上
        token = get_token()
        print('yaml中的token:%s'%token)
        data = str(data).replace("#{token}", token)
        print('login_token:%s' % data)
        re = SendRequests().sendRequests(self.s,eval(data))
        true_status = int(re['status'])
        print('ddt中数据为:%s'%true_status)
        self.assertEqual(true_status,int(expect_result),'实际返回数据为:%s'%re)


if __name__ == '__main__':
    unittest.main()