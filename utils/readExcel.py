from utils.ExcelUtils import OperationExcel

#从表格里读取数据
class ReadExcel():
    def __init__(self):
        self.opExcel = OperationExcel()

    def readExcel(self):
        # 场景
        envTemp = ""
        # 用例
        example = ""

        genKeyValue = ""