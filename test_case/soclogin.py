# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import time
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from securtcode import getCode
from public.log import Logger
from PIL import Image
from conf.remote import RemoteDriver


class TestSocLogin(unittest.TestCase):
    """测试soc登录模块"""
    logger = Logger('INFO')
    url = "https://172.17.1.202/SOC2.0/juum/jnetsystemweb/login.htm"

    def setUp(self):
        remote = RemoteDriver()
        self.driver = remote.driver
        # self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        self.driver.get_screenshot_as_file('../images/%s-%s_code.jpg' % (remote.host.split(':')[0], remote.browser))
        img = self.driver.find_element(By.CLASS_NAME, "security-code-img")
        left = img.location['x']
        top = img.location['y']
        right = img.location['x'] + img.size['width']
        down = img.location['y'] + img.size['height']
        picture = Image.open('../images/%s-%s_code.jpg' % (remote.host.split(':')[0], remote.browser))
        picture = picture.crop((left, top, right, down))
        picture.save('../images/%s-%s_code.png' % (remote.host.split(':')[0], remote.browser))

    def test_right(self):

        """用户名密码正确"""

        self.driver.find_element(By.ID, "txtUserName").clear()
        self.driver.find_element(By.ID, "txtUserName").click()
        self.driver.find_element(By.ID, "txtUserName").send_keys('cfgadmin')

        self.driver.find_element(By.ID, "txtPassword").clear()
        self.driver.find_element(By.ID, "txtPassword").click()
        self.driver.find_element(By.ID, "txtPassword").send_keys('password')

        self.driver.find_element(By.ID, "txtSecurityCode").clear()
        self.driver.find_element(By.ID, "txtSecurityCode").click()

        # url = self.driver.find_element(By.CLASS_NAME, "security-code-img").get_attribute("src")
        # self.logger.info('url:%s' % url)
        get_code = getCode()
        code = get_code.get_securtcode()
        self.driver.find_element(By.ID, "txtSecurityCode").send_keys(code)

        self.driver.find_element(By.CLASS_NAME, "loginbutton").click()
        self.driver.implicitly_wait(30)
        try:
            text = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/ul[1]/li[1]/a/span").text
            self.assertEqual(text, u"态势感知")
        except Exception as msg:
            self.logger.info(u"异常原因%s" % msg)
            now = time.strftime('%Y-%m-%d')
            self.driver.get_screenshot_as_file('../images/soclogin_%s.png' % now)
            self.logger.info('generation screeshot-test_soclogin_%s.png' % now)
            raise

    def tearDown(self):
        self.driver.quit()

'''
if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d')
    path = os.path.abspath('..') + os.sep + 'reports' + os.sep
    report = path + now + '_result.html'
    fp = open(report, 'wb')
    runner = HTMLTestRunnerCN.HTMLTestRunner(
        stream=fp,
        title=u'测试报告',
        tester='Doris'
    )
    suite = unittest.TestSuite()
    suite.addTest(TestSocLogin('test_right'))
    runner.run(suite)
'''
