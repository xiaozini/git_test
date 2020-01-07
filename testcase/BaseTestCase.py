#coding=utf-8
import unittest

from utils.ExcelUtils import OperationExcel


class BaseTestCase(unittest.TestCase):

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