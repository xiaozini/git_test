import unittest,time,os
from common.HTMLTestRunner_PY3 import HTMLTestRunner


def run_case(dir='testcase'):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print('case_dir:%s'%base_dir)
    test_case = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(base_dir+'\\'+dir,pattern="test_*.py",top_level_dir=None)
    return discover

if __name__ == '__main__':
    current_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report_path = os.path.dirname(os.getcwd()) + "\\report\\" + current_time + '.html'  # 生成测试报告的路径
    fp = open(report_path, "wb")
    runner = HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u'qq接口', verbosity=2)
    runner.run(run_case())
    fp.close()