import xlrd
class ReadExcel():
    def readExcel(fileName,SheetName='sheet1'):
        data = xlrd.open_workbook(fileName)
        table = data.sheet_by_name(SheetName)

        #获取总行数 总列数
        nrows = table.nrows
        ncols = table.ncols
        if nrows > 1:
            #获取第一行的内容
            keys = table.row_values(0)

            listApiData = []
            for col in range(1,nrows):
                values = table.row_values(col)
                api_dict = dict(zip(keys,values))
                listApiData.append(api_dict)
            return listApiData
        else:
            print('表格未填写数据')
            return None

# if __name__ == '__main__':
#     s = ReadExcel.readExcel(r'F:\yy\appDemo\yuedao_framework\resource\test_api1.xlsx','login')
#     print(s)