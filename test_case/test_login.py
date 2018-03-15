# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from public.PageObject.loginPage import LoginPage
from selenium.webdriver.common.by import By
from conf.remote import RemoteDriver
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
    username, password = [], []
    logger.info('read csv file')
    with open(data_file, 'r') as f:
        data = csv.reader(f)
        for i, info in enumerate(data):
            username.append(info[0])
            password.append(info[1])
    logger.info('username list: %s' % username)
    logger.info('password list: %s' % password)

    now = time.strftime('%Y-%m-%d')

    def setUp(self):
        self.driver = RemoteDriver().driver
        self.driver.implicitly_wait(30)
        self.login = LoginPage(self.driver)
        self.login.open()

    def test_null_pwd(self):

        u"""密码为空"""

        self.logger.info('username: %s, password: %s' % (self.username[1], self.password[1]))
        try:
            self.login.type_username(self.username[1])
            self.login.type_password(self.password[1])
            self.login.login()
            self.driver.implicitly_wait(10)
            time.sleep(1)
            text = self.login.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span[2]").text
            self.assertEquals(text, u"请输入密码")
        except Exception as msg:
            self.logger.warning("reasons of exception %s" % msg)
            self.driver.get_screenshot_as_file('../images/test_pwd_null_%s.png' % self.now)
            raise

    def test_null_username(self):

        u""""用户名为空"""

        self.logger.info('username: %s, password: %s' % (self.username[2], self.password[2]))
        try:
            self.login.type_username(self.username[2])
            self.login.type_password(self.password[2])
            self.login.login()
            self.driver.implicitly_wait(10)
            text = self.login.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span[1]").text
            self.assertEqual(text, u"请输入邮箱名")
        except Exception as msg:
            self.logger.warning("reasons of exception %s" % msg)
            self.driver.get_screenshot_as_file('../images/test_null_username_%s.png' % self.now)
            raise

    def test_wrong_pwd(self):

        u"""密码错误"""

        self.logger.info('username: %s, password: %s' % (self.username[3], self.password[3]))
        try:
            self.login.type_username(self.username[3])
            self.login.type_password(self.password[3])
            self.login.login()
            self.driver.implicitly_wait(10)
            time.sleep(2)
            text = self.login.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div[2]/div/div/div[4]/div[1]/div[1]/div[1]/span[1]").text
            self.assertEqual(text, u"登录名或密码错误")
        except Exception as msg:
            self.logger.warning("reasons of exception %s" % msg)
            self.driver.get_screenshot_as_file('../images/test_wrong_pwd_%s.png' % self.now)
            raise

    def test_right(self):

        u"""成功登陆"""

        self.logger.info('username:%s, password: %s' % (self.username[0], self.password[0]))
        try:
            self.login.type_username(self.username[0])
            self.login.type_password(self.password[0])
            self.login.login()
            self.driver.implicitly_wait(10)
            time.sleep(1)
            text = self.login.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div[4]/div[1]/div[3]/div[1]/span/em[2]").text
            self.assertEqual(text, self.username[0])
        except Exception as msg:
            self.logger.warning("reasons of exception %s" % msg)
            self.driver.get_screenshot_as_file('../images/test_right_%s.png' % self.now)
            self.logger.info('generation scree shot-test_right_%s.png' % self.now)
            raise

    def tearDown(self):
        self.driver.quit()
