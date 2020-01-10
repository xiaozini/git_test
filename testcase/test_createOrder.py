from common.readExcel import ReadExcel
import os,yaml
import unittest,requests
from readConfig import ReadConfig
from common.read_token import get_token
from ddt import ddt,data
from common.readRequests import SendRequests

baseUrl = ReadConfig().get_config('HTTP',"newurl")
path = os.path.join(os.path.dirname(os.getcwd()),'resource','test_api1.xlsx')
testcast = ReadExcel.readExcel(path,'createorder')

#获取根目录
ypath = os.path.join(os.path.dirname(os.getcwd()),'common','order.yaml')
print('根目录为:%s'%ypath)

@ddt
class TestOrderPage(unittest.TestCase):
    def setUp(self):
        self.s = requests.session()
    def tearDown(self):
        pass

    @data(*testcast)
    def test_api(self,data):
        expect_result = int(data['expect_result'].split(':')[1])
        # 获取token 并放在yaml上
        token = get_token()
        print('yaml中的token:%s'%token)
        data = str(data).replace("#{token}", token)
        print('login_token:%s' % data)
        re = SendRequests().sendRequests(self.s,eval(data),baseUrl)
        true_status = int(re['status'])
        if true_status == 1:
            #获取token 并放在yaml上
            orderNo = re['data']
            print('orderNo:%s'%orderNo)
            with open(ypath,'w',encoding='utf-8') as f:
                yaml.dump(orderNo,f)

        self.assertEqual(expect_result,true_status,'实际返回数据为:%s'%re)
        lines = ReadExcel().get_lines()
        for line in len(lines):
            ReadExcel().write_cell_value(path,"createorder",line, 16, re)



if __name__ == '__main__':
    unittest.main()