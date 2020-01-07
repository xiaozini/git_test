#coding=utf-8
import unittest
import requests,os
import json,urllib3
from utils.ExcelUtils import OperationExcel
from common.read_token import get_token

class TestLogin(unittest.TestCase):


    def setUp(self):
        # 读取表格
        self.excelUtil = OperationExcel(1)
        # sheet_0
        self.sheet_0 = self.excelUtil.get_exceldata()
        print('self.sheet_0;'.format(self.sheet_0))
        # # 黄色标题列清除
        # for i in range(self.excelUtil.get_lines() - 1):
        #     # row = self.sheet_0.row_values(i + 1)
        #     self.excelUtil.write_cell_value(i + 1, 12, "")
        #     self.excelUtil.write_cell_value(i + 1, 13, "")
        #     self.excelUtil.write_cell_value(i + 1, 14, "")
        #     self.excelUtil.write_cell_value(i + 1, 15, "")


    def testUserInfo(self):
        urllib3.disable_warnings()
        # 场景
        envTemp = ""
        # 用例
        example = ""

        genKeyValue = ""
        row = self.sheet_0.row_values(1)
        if row[1] != "":
            envTemp = row[1]

        if row[2] != "":
            example = row[2]

        print("开始 场景:" + envTemp + ",用例:" + example)

        # 处理是否运行
        # if "Y" != row[4]:
        #     print("结束 场景:" + envTemp + ",用例:" + example + "，原因: 是否运行：N")
        #     continue

        # 1 调用发起前 参数搜集/检查
        # 是否需要token
        body = row[8]
        body = json.loads(body)
        print('body:'.format(body))
        #登录成功返回的token替换
        login_token = get_token()
        print('login_token:'+login_token)
        token = body["protocol"]["token"]
        print('token:'.format(token))
        if token != login_token:
            token = login_token
            print('token11:'.format(token))

        # 2 发起调用 需要什么参数  url method header body
        url = row[3]
        method = row[6]
        header = row[7]

        result = ""
        if "post" == method:
            result = requests.post(url=url, json = body, headers=json.loads(header), verify=False)
        elif "get" == method:
            result = requests.get(url=url, params=json.loads(body), headers=json.loads(header), verify=False)
        else:
            print("unknown method!")
            # continue

        resultJson = result.json()
        print("返回结果:", resultJson)
        # 实际结果写入表格
        self.excelUtil.write_cell_value(1, 13, str(resultJson))

        # 3 结果处理
        exceptResult = row[9]
        # 3.1 结果是否通过
        if result.status_code == 200:
            # 如果预期结果不止一个code TODO 支持多个参数结果检查
            if resultJson["status"] == int(exceptResult.split(":")[1]):
                self.excelUtil.write_cell_value(1, 14, "Y")

                print("结束 场景:" + envTemp + ",用例:" + example + ',参数为：' + genKeyValue)
            else:
                self.excelUtil.write_cell_value(1, 14, "N")
        elif resultJson["status"] == "":
            print('运行失败：' + str(resultJson))

    def testUserInfoFalse(self):
        urllib3.disable_warnings()
        # 场景
        envTemp = ""
        # 用例
        example = ""

        row = self.sheet_0.row_values(2)
        if row[1] != "":
            envTemp = row[1]

        if row[2] != "":
            example = row[2]

        print("开始 场景:" + envTemp + ",用例:" + example)

        # # 处理是否运行
        # if "Y" != row[4]:
        #     print("结束 场景:" + envTemp + ",用例:" + example + "，原因: 是否运行：N")
        #     continue

        # 1 调用发起前 参数搜集/检查
        # 是否需要token
        body = row[8]

        # 2 发起调用 需要什么参数  url method header body
        url = row[3]
        method = row[6]
        header = row[7]

        result = ""
        if "post" == method:
            result = requests.post(url=url, json=json.loads(body), headers=json.loads(header), verify=False)
        elif "get" == method:
            result = requests.get(url=url, params=json.loads(body), headers=json.loads(header), verify=False)
        else:
            print("unknown method!")
            # continue

        resultJson = result.json()
        print("返回结果:", resultJson)
        # 实际结果写入表格
        self.excelUtil.write_cell_value(2, 13, str(resultJson))

        # 3 结果处理
        exceptResult = row[9]
        # 3.1 结果是否通过
        if result.status_code == 200:
            # 如果预期结果不止一个code TODO 支持多个参数结果检查
            if resultJson["status"] == int(exceptResult.split(":")[1]):
                self.excelUtil.write_cell_value(2, 14, "Y")
            else:
                self.excelUtil.write_cell_value(2, 14, "N")
        elif resultJson["status"] == "":
            print('运行失败：' + str(resultJson))



if __name__ == '__main__':
    # TestLogin().testLogin()
    unittest.main()
    # filename = '../result/report.html'
    # fp = open(filename,'wb')
    # suit = unittest.TestSuite()
    # suit.addTests(TestLogin("testUserInfo"),TestLogin("testUserInfoFalse"))
    # runner = HTMLTestRunner.run(stream = fp,title='测试报告',
    #                    description='接口自动化测试报告')
    # runner.run(suit)
    # fp.close()

