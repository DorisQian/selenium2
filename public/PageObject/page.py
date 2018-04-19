# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from public.log import log
from conf.configure import conf
from selenium import webdriver
#from public.se_rc import driver
from conf.remote import RemoteDriver
import time
import os

__author__ = 'Doris Qian'


class Page(object):
    u"""
    基本类，用于所有页面的继承
    """

    def __init__(self):
        self._logger = log(os.path.basename(__file__))
        self.remote = RemoteDriver()
        self.driver = self.remote.driver
        self.host = self.remote.host
        self._base_url = conf['url']

    def _open(self):
        # new_url = self._base_url + url
        self.driver.get(self._base_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        time.sleep(1)
        assert self.on_page() == True, "The page does not open correctly"

    def open(self):
        u"""
        打开页面url
        :return:
        """
        return self._open()

    def on_page(self):
        u"""
        判断当前url和传入url是否相同
        :return:
        """
        return self.driver.current_url == self._base_url

    def find_element(self, *loc):
        u"""
        定位元素
        :param loc:定位方式
        :return:
        """
        return self.driver.find_element(*loc)

    def send_keys(self, *loc, value, clear_first=True, click_first=True):
        u"""
        传入文字
        :param loc:定位
        :param value: 传入的内容
        :param clear_first: 是否先清空
        :param click_first: 是否先点击
        :return:
        """
        try:
            # loc = getattr(self, '_%s' % loc)
            if clear_first:
                self.find_element(*loc).clear()
            if click_first:
                self.find_element(*loc).click()
            self.find_element(*loc).send_keys(value)
            time.sleep(1)
        except AttributeError:
            self._logger.error('%s page does not have "%s" locator' % loc)

    def close(self):
        self.driver.quit()

