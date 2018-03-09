# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import unittest
import time
import HTMLTestRunner
import logging
import os
from public.log import Logger

__author__ = "Doris Qian"


logger = Logger(logname='log.txt', loglevel="INFO", logger="run.py")


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
runner = HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    title=u'新浪邮箱测试报告',
    description=u'用例执行情况：')

if __name__ == '__main__':
    alltestnames = createsuit()
    runner.run(alltestnames)
    fp.close()