import xlrd
from xlutils.copy import copy
# import sys
# print(sys.path)

class OperationExcel:

    def __init__(self,sheetid=None,filename=None):
        if filename:
            self.filename = filename
            self.sheetid = sheetid
        else:
            self.filename = '../resource/test_api1.xlsx'
            self.sheetid = 0
        self.data = self.get_exceldata()

    #获取sheets内容
    def get_exceldata(self):
        data = xlrd.open_workbook(self.filename)
        sheet_0 = data.sheets()[self.sheetid]
        return sheet_0

    #获取单元格的行数
    def get_lines(self):
        tables = self.data
        return tables.nrows

    #获取某一个单元格的内容
    def get_cell_value(self,row,col):
        return self.data.cell_value(row,col)

    #在某单元格写内容
    def write_cell_value(self,row,col,value):
        read_data = xlrd.open_workbook(self.filename)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row,col,value)
        write_data.save(self.filename)

    #1.根据对应的caseid找到对应行的内容
    def get_rows_data(self,case_id):
        row_num = self.get_row_num(case_id)
        rows_data = self.get_row_value(row_num)
        return rows_data

    #2.根据对应的caseid找到对应的行号
    def get_row_num(self,case_id):
        num = 0
        cols_data = self.get_cols_data()
        for col_data in cols_data:
            if case_id in col_data:
                return num#行号
            num = num + 1

    #根据行号，找到该行的内容
    def get_row_value(self,row):
        tables = self.data
        row_data = tables.row_values(row)#行的内容
        return row_data

    #获取某一列的内容
    def get_cols_data(self,col_id=None):
        if col_id != None:#列号
            cols = self.data.col_values(col_id)
        else:
            cols = self.data.col_values(0)#获取第0列的内容
        return cols

    def get_Row(self,rowId):
        sheet0 = self.get_exceldata()
        for i in range(self.get_lines() - 1):
            row = sheet0.row_values(i + 1)
            if row[0] == rowId:
                return row