import xlrd,xlwt
from xlutils.copy import copy

class ReadExcel():

    #获取sheets内容
    # def get_exceldata(self,filename,sheetName='sheet1'):
    #     self.data = xlrd.open_workbook(filename)
    #     sheet = self.data.sheet_by_name(sheetName)
    #     return sheet

    def readExcel(self,filename,sheetName='sheet1'):
        self.data = xlrd.open_workbook(filename)
        self.table = self.data.sheet_by_name(sheetName)

        #获取总行数 总列数
        nrows = self.table.nrows
        if nrows > 1:
            #获取第一行的内容
            keys = self.table.row_values(0)

            listApiData = []
            for col in range(1,nrows):
                values = self.table.row_values(col)
                api_dict = dict(zip(keys,values))
                listApiData.append(api_dict)
            return listApiData
        else:
            print('表格未填写数据')
            return None

# 在某单元格写内容
    def write_cell_value(self,filename):
        read_data = xlrd.open_workbook(filename,formatting_info=True)
        new_data = copy(read_data)
        sheet_data = new_data.get_sheet(0)
        sheet_data.write(3, 15, "晓可")
        new_data.save(filename)

    def write_cell_values(self,filename,sheet,row,col,values):
        xls = xlwt.Workbook()
        sheet= xls.add_sheet(sheet)
        sheet.write(row,col,values)
        xls.save(filename)

    #获取单元格的行数
    def get_lines(self):
        tables = self.sheetid
        return tables.nrows


if __name__ == '__main__':
    readExcel = ReadExcel()
    # s = readExcel.readExcel(r'F:\yy\appDemo\yuedao_framework\resource\test_api1.xlsx','login')
    readExcel.write_cell_value(r'F:\yy\appDemo\yuedao_framework\resource\test_api1.xlsx')
    s = readExcel.readExcel(r'F:\yy\appDemo\yuedao_framework\resource\test_api1.xlsx', 'login')
    print(s)