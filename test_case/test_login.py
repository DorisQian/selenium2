# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from public.PageObject.loginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium import webdriver
from public.log import Logger
import time
import unittest
import csv
import os

__author__ = 'Doris Qian'


class TestLogin(unittest.TestCase):

    u"""测试登录模块"""

    logger = Logger('INFO')
    path = os.path.abspath('..') + os.sep + 'conf' + os.sep
    data_file = path + 'data.csv'
    # with open(data_file, 'rb') as f:
        # data = csv.reader(f)
    data = csv.reader(open(data_file, 'r'))
    logger.info('read csv file')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        # self.base_url = "https://mail.sina.com.cn/"
        # self.driver.get(self.base_url)

    def test_right(self):

        u"""成功登陆"""

        for i, info in enumerate(self.data):
            if i == 0:
                print(info)
                username = info[0]
                password = info[1]
                self.logger.info('username:%s, password: %s' % (username, password))
        try:
            login = LoginPage(self.driver)
            login.open()
            login.type_username(username)
            login.type_password(password)
            login.login()
            self.driver.implicitly_wait(10)
            time.sleep(1)
            text = login.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div[3]/div[1]/span/em[2]").text
            self.assertEqual(text, username)
        except Exception as msg:
            self.logger.warning("reasons of exception %s" % msg)
            now = time.strftime("%Y-%m-%d_%H:%M:%S")
            self.driver.get_screenshot_as_file('../images/testlogin_%s.png' % now)
            self.logger.info('generation screeshot-testlogin_%s.png' % now)
            raise

    def test_pwdnull(self):
        for i, info in enumerate(self.data):
            if i == 1:
                username = info[0]
                password = info[1]
                self.logger.info('username: %s, password: %s' % username, password)
        try:
            login = LoginPage(self.driver)
            login.open()
            login.type_username(username)
            login.type_password(password)
            login.login()


    def setDown(self):
        self.data.close()
        self.driver.quit()
