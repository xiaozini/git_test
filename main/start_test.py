#coding=utf-8

# 测试入口
import urllib3
from common.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.ExcelUtils import OperationExcel
import requests
import json
import unittest
class TestMethod():
    Login_token = "MTk3NHwxNTc5MjQzODU1MzgzfPx0BM7Xqb_pXEoajcKRH9BQ2QIIsyuIym9d2XqeO-fL"
    def __init__(self):
        # 读取表格
        self.excelUtil = OperationExcel()
        # sheet_0
        self.sheet_0 = self.excelUtil.get_exceldata()
        # 黄色标题列清除
        for i in range(self.excelUtil.get_lines() - 1):
            # row = self.sheet_0.row_values(i + 1)
            self.excelUtil.write_cell_value(i + 1, 12, "")
            self.excelUtil.write_cell_value(i + 1, 13, "")
            self.excelUtil.write_cell_value(i + 1, 14, "")
            self.excelUtil.write_cell_value(i + 1, 15, "")

    def test01(self):
        urllib3.disable_warnings()
        # 场景
        envTemp = ""
        # 用例
        example = ""

        genKeyValue = ""
        for i in range(self.excelUtil.get_lines()-1):
            row = self.sheet_0.row_values(i+1)
            if row[1] != "":
                envTemp = row[1]

            if row[2] != "":
                example = row[2]

            print("开始 场景:" + envTemp + ",用例:" + example)

            # 处理是否运行
            if "Y" != row[4] :
                print("结束 场景:" + envTemp + ",用例:" + example + "，原因: 是否运行：N")
                continue

            # 1 调用发起前 参数搜集/检查
            # 是否需要token
            body = row[8]
            isToken = row[5]
            if "Y" == isToken:
                # TODO 如果需要TOKEN
                global Login_token
                Login_token = "MTk3NHwxNTc5MjQzODU1MzgzfPx0BM7Xqb_pXEoajcKRH9BQ2QIIsyuIym9d2XqeO-fL"
                if "" == Login_token:
                    print("Login_token 为空！")
                else:
                    print("Login_token : " + Login_token)
                    body = body.replace("#{token}", Login_token)
                    pass




            # 2 发起调用 需要什么参数  url method header body
            url = row[3]
            method = row[6]
            header = row[7]
            # 引用其他接口返回结果
            refKey = row[10]


            print('body类型为:',type(body))
            if "" != refKey:
                # TODO 获取其他参数返回结果
                for refKeyValue in refKey.split(","):
                    kvs = refKeyValue.split(".")
                    rowId = kvs[0]
                    genKey = kvs[1]
                    tempRow = self.getRow(rowId)
                    print('tempRow:',tempRow)
                    genKeyValues = tempRow[12]
                    print('genKeyValues:',genKeyValues)
                    for genKeyValue in genKeyValues.split(","):
                        if genKeyValue != "" and ":" in genKeyValue:
                            genkvs = genKeyValue.split(":")
                            genkvs_key = genkvs[0]
                            genkvs_value = genkvs[1]
                            print("genkvs_key:",genkvs_key)
                            print('genkvs_value:',genkvs_value)
                            if genKey == genkvs_key:
                                body = body.replace("#{" + genKey + "}", genkvs_value)

            print('请求参数body为:', body)

            # TODO body中的占位符替换

            result = ""
            if "post" == method:
                result = requests.post(url=url,json=json.loads(body),headers=json.loads(header),verify=False)
            elif "get" == method:
                result = requests.get(url=url,params=json.loads(body),headers=json.loads(header),verify=False)
            else:
                print("unknown method!")
                continue

            resultJson = result.json()
            print("返回结果:",resultJson)
            # 实际结果写入表格
            self.excelUtil.write_cell_value(i+1, 13, str(resultJson))

            # 3 结果处理
            exceptResult = row[9]
            # 3.1 结果是否通过
            if result.status_code == 200 :
                # 如果预期结果不止一个code TODO 支持多个参数结果检查
                # if resultJson["status"] != "":
                #     print('运行失败：'+resultJson)
                if resultJson["status"] == int(exceptResult.split(":")[1]):
                    self.excelUtil.write_cell_value(i+1, 14, "Y")
                    # 3.2 返回信息 参数化
                    genKey = row[11]
                    if genKey != "":
                        # TODO 考虑多参数/参不在data层 结果->参数
                        genKeyValue = genKey + ":" + resultJson[genKey]
                        print('参数化的genkeyValue为;', genKeyValue)
                        self.excelUtil.write_cell_value(i + 1, 12, genKeyValue)
                    print("结束 场景:" + envTemp + ",用例:" + example + ',参数为：' + genKeyValue)
                else:
                    self.excelUtil.write_cell_value(i+1, 14, "N")
            elif resultJson["status"] == "":
                print('运行失败：' + str(resultJson))

            # 3.2 返回信息 参数化
            # if row[14] == "Y":
            #     genKey = row[11]
            #     if genKey != "" :
            #         # TODO 考虑多参数/参不在data层 结果->参数
            #         genKeyValue = genKey + ":" + resultJson["data"][genKey]
            #         print('参数化的genkeyValue为;',genKeyValue)
            #         self.excelUtil.write_cell_value(i + 1, 12, genKeyValue)
            #     print("结束 场景:" + envTemp + ",用例:" + example+',参数为：'+ genKeyValue)
            # elif row[14] == 'N':
            #     pass

        pass

    def getRow(self,rowId):
        sheet0 = self.excelUtil.get_exceldata()
        for i in range(self.excelUtil.get_lines() - 1):
            row = sheet0.row_values(i + 1)
            if row[0] == rowId:
                return row

    # def tearDown(self):
    #     pass

if __name__ == '__main__':
    TestMethod().test01()

    # fileName = r"F:\yy\appDemo\yuedao_framework\report\htmlResult.html"
    # with open(fileName,"wb") as f:
    #     suite = unittest.TestSuite()
    #     suite.addTest(TestMethod("test01"))
    #     runner = HTMLTestRunner(stream=f,title="接口自动化测试报告",description="测试结果为:")
    #     runner.run(suite)




