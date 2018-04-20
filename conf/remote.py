# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from selenium.webdriver import Remote
from public.log import log
import os


class RemoteDriver:

    _lists = {'http://172.17.1.205:5556/wd/hub': 'chrome'}
    logger = log(os.path.basename(__file__))

    for host, browser in _lists.items():
        browser = browser
        logger.info('host:%s,browser:%s' % (host, browser))
        driver = Remote(command_executor=host,
                        desired_capabilities={'platform': 'ANY',
                                              'browserName': browser,
                                              'version': '',
                                              'javascriptEnable': True
                                              }
                        )

