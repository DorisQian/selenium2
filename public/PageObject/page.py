# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import time

__author__ = 'Doris Qian'


class Page(object):
    """
    基本类，用于所有页面的继承
    """
    login_url = "https://mail.sina.com.cn/"

    def __init__(self, driver, base_url=login_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        # new_url = self.base_url + url
        self.driver.get(self.base_url)
        time.sleep(2)
        assert self.on_page() == True, "The page does not open correctly"

    def on_page(self):
        print(self.driver.current_url)
        return self.driver.current_url == self.base_url

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def send_keys(self, loc, value, clear_first=True, click_first=True):
        # loc = getattr(self, loc)
        if clear_first:
            self.find_element(*loc).clear()
        if click_first:
            self.find_element(*loc).click()
        self.find_element(*loc).send_keys(value)


