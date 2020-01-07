#coding=utf-8
import unittest
import os
from common.HTMLTestRunner_PY3 import *

root_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
testcase_path = os.path.join(root_path, "testcase")

def all_case():
    discover = unittest.defaultTestLoader.discover(testcase_path,pattern="*.py",top_level_dir=None)
    return discover

if __name__ == '__main__':
    file = '../result/report.html'
    with open(file,'wb')as f:
        runner = HTMLTestRunner(f,title='接口测试报告',description='测试用例情况')
        runner.run(all_case())