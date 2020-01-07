#coding=utf-8
import unittest
import readConfig
import os
from common.Log import MyLog
import HTMLTestRunner

localReadConfig = readConfig.ReadConfig()

class AllTest:

    def __init__(self):
        global log,logger,resultPath,on_off
        log = MyLog.get_log()
        logger = log.get_logger()
        resultPath = log.get_result_path()
        self.caseListFile = os.path.join(readConfig.proDir,'caselist.txt')
        self.caseFile = os.path.join(readConfig.proDir,'testCase')
        self.caseList = []

    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != "" and not data.startswith("#"):
                self.caseList.append(data.replace("\n",""))
        fb.close()

    def set_case_suite(self):
        self.set_case_list()
        test_suite = unittest.TestSuite()
        print('test_suite为:'.format(test_suite))
        suite_module = []
        for case in self.caseList:
            case_name = case.split("/")[-1]
            discover = unittest.defaultTestLoader.discover(self.caseFile,
                                                           pattern=case_name+".py",top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        try:
            suit = self.set_case_suite()
            if suit is not None:
                with open(resultPath,'wb') as fp:
                    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                                           title='Test Report',description='Test Description')
                    runner.run(suit)
            else:
                logger.info('have no case to test')
        except Exception as e:
            logger.error(str(e))



if __name__ == '__main__':
    obj = AllTest()
    obj.run()
