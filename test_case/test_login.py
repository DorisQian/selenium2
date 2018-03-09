# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from public.PageObject.loginPage import LoginPage
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import unittest
import csv

__author__ = 'Doris Qian'


class TestLogin(unittest):
    """
    测试登录模块
    """
    data_file = '../conf/data.csv'
    data = csv.reader(data_file, 'rb')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://mail.sina.com.cn/"

    # 输入正确用户名密码
    def test_right(self):
        for i, info in enumerate(self.data):
            if i == 1:
                print(info)
                username = info[0]
                password = info[1]
        try:
            self.driver.get(self.base_url)
            login = LoginPage(driver)
            login.open()
            login.type_username(username)
            login.type_password(password)
            login.login()
            self.driver.implicitly_wait(10)
            time.sleep(1)
            text = login.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div[3]/div[1]/span/em[2]").text
            self.assertEqual(text, username)
        except Exception as msg:
            logging.info(u"异常原因%s" % msg)
            now = time.strftime("%Y-%m-%d_%H:%M:%S")
            self.driver.get_screenshot_as_file('../images/testlogin_%s.jpg' % now)
            raise

    def setDown(self):
        self.driver.quit()
