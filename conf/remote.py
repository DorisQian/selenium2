# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from selenium.webdriver import Remote
from public.log import Logger

lists = {'http://172.17.1.207:5555/wd/hub': 'chrome'}
logger = Logger('INFO')


class RemoteDriver():
    def __init__(self):
        for host, browser in lists.items():
            self.host = host.rstrip('/wd/hub')
            self.browser = browser
            logger.info('host:%s,browser:%s' % (host, browser))
            self.driver = Remote(command_executor=host,
                                 desired_capabilities={'platform': 'ANY',
                                                       'browserName': browser,
                                                       'version': '',
                                                       'javascriptEnable': True
                                                       })

