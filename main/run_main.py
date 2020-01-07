#coding=utf-8
from utils.ExcelUtils import OperationExcel
import requests,json


class RunMain():
    def __init__(self):
        self.operaExcel = OperationExcel()
        self.sheet = self.operaExcel.get_exceldata()
        for i in range(self.operaExcel.get_lines()-1):
            self.operaExcel.write_cell_value(i+1,12,"")
            self.operaExcel.write_cell_value(i+1,13, "")
            self.operaExcel.write_cell_value(i+1,14,"")
            self.operaExcel.write_cell_value(i+1,15, "")

    def run(self):
        #场景
        exampleCode = ""
        #用例
        example = ""

        # 循环表数据，执行请求
        for i in range(self.operaExcel.get_lines() - 1):
            # 根据行号获取该行的内容
            row_data = self.sheet.row_values(i + 1)
            if row_data[1] != "":
                exampleCode = row_data[1]

            if row_data[2] != "":
                example = row_data[2]
            print('测试模块为:' + exampleCode + ",用例名为：" + example)

            #是否携带token
            if row_data[5] == 'N':
                pass

            if row_data[8] != "":
                request_data = row_data[8]

            if row_data[3] != "":
                url = row_data[3]

            if row_data[7] != "":
                isHeader = row_data[7]

            if row_data[6] != "":
                method = row_data[6]

            if row_data[4] != "":
                isRun = row_data[4]

            if row_data[11] != "":
                responseKey = row_data[11]

            #引用的key
            needKey = row_data[10]

            if needKey != "":
                for needKeyValue in needKey.split(","):
                    # 获取值
                    needKey_Values = needKeyValue.split(".")
                    getExampleId = needKey_Values[0]
                    getResponseKey = needKey_Values[1]
                    # 根据exampleId 获取整行数据
                    rowData = self.operaExcel.get_Row(getExampleId)
                    # 拿到该行提供的key value值
                    responseKeyValues = rowData[12]

                    for responseKeyValue in responseKeyValues.split(','):
                        if responseKeyValue != "" and ":" in responseKeyValue:
                            genkvs = responseKeyValue.split(":")
                            genkvs_key = genkvs[0]
                            genkvs_value = genkvs[1]
                            print('返回的key:'+genkvs_key+",返回key对应的值为:"+genkvs_value)
                            # 判断需要引用的key和提供的key值是否相同
                            if genkvs_key == getResponseKey:
                                # 把提供的value值替换params里的值
                                request_data = request_data.replace("#{" + getResponseKey + "}", genkvs_value)

            result = ""  # 实际结果
            print("-------------")
            print(type(request_data))
            print("请求参数为:" + str(request_data))

            if isRun == 'Y':#执行
                if method == 'post':
                    result = requests.post(url = url,json = json.loads(request_data),headers = json.loads(isHeader))
                elif method == 'get':
                    result = requests.get(url= url,params = json.loads(request_data),headers = json.loads(isHeader))

                else:
                    print("请求方法为:",method)

                resultJson = result.json()

                # 把结果写到表格里
                self.operaExcel.write_cell_value(i+1, 13, str(resultJson))

                if row_data[14] != "":
                    isPass = row_data[14]

                expectResult = ""  # 预期结果
                if row_data[9] != "":
                    expectResult = row_data[9]

                #预期 实际结果的判断
                print('返回数据为:%s'%result)
                if result.status_code == 200:
                    if int(expectResult.split(":")[1]) == resultJson["status"]:
                        self.operaExcel.write_cell_value(i+1,14,"Y")
                    else:
                        self.operaExcel.write_cell_value(i + 1, 14, "N")

             #返回信息  参数化
                if row_data[14] == "Y":
                    getResponseKey = row_data[11]
                    if getResponseKey != "":
                        genkvs_value = getResponseKey+":" + resultJson["data"][getResponseKey]
                        print("参数化值为:"+genkvs_value)
                        self.operaExcel.write_cell_value(i+1,12,genkvs_value)
                    print("结束 场景:" + exampleCode + ",用例:" + example + ',参数为：' + genkvs_value)

if __name__ == '__main__':
    RunMain().run()