# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import unittest
import time
import logging
import os
from public.log import Logger
import HTMLTestRunnerCN
from public.send_mail import SendMail
from conf.remote import RemoteDriver

__author__ = "Doris Qian"


logger = Logger('DEBUG')


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

runner = HTMLTestRunnerCN.HTMLTestRunner(
    stream=fp,
    title=u'新浪邮箱测试报告',
    tester=u'Doris')

if __name__ == '__main__':
    all_tests = createsuit()
    runner.run(all_tests)
    fp.close()
    flag = SendMail().pack_images()
    logger.debug('flag is %s' % flag)
    remote = RemoteDriver()
    host = (remote.host, remote.browser)
    SendMail().send_report(path, flag, host)


