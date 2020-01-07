# 测试入口
#coding=utf-8
from utils.ExcelUtils import OperationExcel
import requests
import json

class my_test:

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


    def run(self):
        #场景
        envTemp = ""
        #用例
        example = ""

        for i in range(self.excelUtil.get_lines()-1):
            row = self.sheet_0.row_values(i + 1)
            if row[1] != "":
                envTemp = row[1]

            if row[2] != "":
                example = row[2]

            print("开始 场景:"+envTemp+",用例："+example)

            #处理是否运行
            if "Y" != row[4]:
                print('结束场景：' + envTemp+",用例:"+example+",原因为:"+row[4])
                continue

            #1.调用发起前  参数搜集/检查
            #是否需要token
            isToken = row[5]
            if "Y" == isToken:
                pass

            #2.发起调用 需要的参数
            url = row[3]
            method = row[6]
            header = row[7]

            #引用其他接口返回结果
            refKey = row[10]

            body = row[8]
            print("请求参数为:"+body)

            if "" != refKey:
                for refKeyValue in refKey.split(","):
                    kvs = refKeyValue.split(".")
                    rowId = kvs[0]
                    genKey = kvs[1]
                    tempRow = self.getRow(rowId)
                    genKeyValues = tempRow[12]
                    for genKeyValue in genKeyValues.split(","):
                        if genKeyValue != "" and genKeyValue.contains(":"):
                            genkvs = genKeyValue.split(":")
                            genkvs_key = genkvs[0]
                            genkvs_value = genkvs[1]
                            if genKey == genkvs_value:
                                body = body.replace("#{"+genKey+"}",genkvs_value)
            print("请求参数body为:"+body)

            result = ""
            if "post" == method:
                result = requests.post(url=url,json=json.loads(body),headers = json.loads(header))
            elif "get" == method:
                result = requests.get(url = url,json=json.loads(body),headers=json.loads(header))
            else:
                print("unknown method")
                continue

            resultJson = result.json()
            print("返回的结果为:"+str(resultJson))
            #实际结果写入表格
            self.excelUtil.write_cell_value(i+1,13,str(resultJson))

            #3.结果处理
            excpetResult = row[9]
            #3.1 结果是否通过
            if result.status_code != 200:
                pass

            #如果预期结果不止一个code
            if resultJson["status"] != "":
                print("运行失败:"+str(resultJson))
            elif resultJson["code"] == int(excpetResult.split(":")[1]):
                self.excelUtil.write_cell_value(i+1,14,"Y")
            else:
                self.excelUtil.write_cell_value(i+1,14,"N")

            #3.2返回信息 参数化
            genKey = row[11]
            if genKey != "":
                #TODO 考虑多参数/参数不在data层 结果——》参数
                genKeyValue = genKey+":"+resultJson["data"][genKey]
                print("参数化的genKeyValue为:"+genKeyValue)
                self.excelUtil.write_cell_value(i+1,12,genKeyValue)
            print("结束场景:"+envTemp+",用例："+example+"，参数为:"+genKeyValue)




    def getRow(self,rowId):
        sheet0 = self.excelUtil.get_exceldata()
        for i in range(self.excelUtil.get_lines() - 1):
            row = sheet0.row_values(i + 1)
            if row[0] == rowId:
                return row


if __name__ == "__main__":
    my_test().run()