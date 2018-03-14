# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from selenium.webdriver import Remote
from public.log import Logger

lists = {'http://172.17.1.207:5555/wd/hub': 'chrome'}
logger = Logger('INFO')

for host, browser in lists.items():
    logger.info('host:%s,browser:%s' % (host, browser))
    driver = Remote(
        command_executor=host,
        desired_capabiltiies={'platform': 'ANY',
                              'browserName': browser,
                              'version': '',
                              'javascriptEnable': True
                              })
