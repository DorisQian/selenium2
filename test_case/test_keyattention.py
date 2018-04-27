# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.conpage import ConPage
from public.dataConnect import Database
from public.login import Login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import math
import time
import os


class KeyAttention(unittest.TestCase):
	u"""测试重点关注"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test key attention')
		cls.now = time.strftime('%Y-%m-%d')
		cls.data = Database()
		cls.login = Login()
		cls.login.login()
		cls.browser = ConPage()
		cls.driver = cls.browser.driver
		try:
			cls.browser.sys_conf()
			cls.driver.implicitly_wait(10)
			cls.browser.function_conf()
			cls.driver.implicitly_wait(10)
			cls.browser.keyattention()
			cls.driver.implicitly_wait(10)
			cls.driver.switch_to.frame('iframepage')
			cls.driver.implicitly_wait(10)
			text = cls.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/table/tbody/tr/td/div[1]/label').text
			assert text == u'重点关注'
		except Exception as msg:
			cls.logger.warning("assert failed: %s" % msg)
			cls.driver.get_screenshot_as_file(
				'../images/keyattention_%s.png' % cls.now)
			raise

	def test_null_query(self):
		u"""测试查询条件为空时查询"""
		self.logger.info('test_null_query')
		records = self.data.count('nmp_keyattention')
		page = math.ceil(records / 20)
		# time.sleep(1)
		self.driver.find_element(By.CLASS_NAME, 'aui-btn-save').click()
		time.sleep(1)
		judge = '一共%s页,共%s条记录' % (page, records)
		text = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/center/div/div').text
		self.assertEqual(text, judge)

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		cls.data.close()