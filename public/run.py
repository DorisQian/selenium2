# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import unittest
import time
# import HTMLTestRunner
import logging
import os
from public.log import Logger
import HTMLTestReportCN

__author__ = "Doris Qian"


logger = Logger('INFO')


def createsuit():
    testunit = unittest.TestSuite()
    test_dir = '../test_case'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py', top_level_dir=None)
    for case in discover:
        logging.info('add case', case)
        testunit.addTest(case)
    return testunit

now = time.strftime("%Y-%m-%d_%H-%M-%S")
path = os.path.abspath('..') + os.sep + 'reports' + os.sep
filename = path + now + '_result.html'
fp = open(filename, 'wb')

logger.info('generated testing report: %s' % filename)

runner = HTMLTestReportCN.HTMLTestRunner(
    stream=fp,
    title=u'新浪邮箱测试报告',
    tester=u'Doris')

if __name__ == '__main__':
    alltests = createsuit()
    runner.run(alltests)
    fp.close()