# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.loginpage import LoginPage
from selenium.webdriver.common.by import By
from public.dataConnect import Database
from conf.configure import conf
from suds.client import Client
import unittest
import xlrd
import time
import os


class TestLogin(unittest.TestCase):
	u"""测试登录模块"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.data = Database()
		cls.logger.info('start test login···')
		file = os.path.abspath('..') + os.sep + 'conf' + os.sep + 'cases.xlsx'
		data = xlrd.open_workbook(file)
		login_sheet = data.sheet_by_name(u'登录')
		cls.username = login_sheet.col_values(5)
		cls.password = login_sheet.col_values(6)
		cls.security = login_sheet.col_values(7)
		cls.browser = LoginPage()
		cls.browser.open()
		cls.driver = cls.browser.driver
		cls.now = time.strftime('%Y-%m-%d')

	def test_null_all(self):
		u"""用户名、密码、验证码均为空"""
		try:
			self.browser.type_username(self.username[1])
			self.browser.type_password(self.password[1])
			self.browser.type_security(self.security[1])
			self.logger.info('username, password, security: %s, %s, %s' % (self.username[1], self.password[1], self.security[1]))
			self.browser.login()
			text = self.driver.find_element(By.CLASS_NAME, 'warn').text
			self.assertEqual(text, u'用户名、密码、验证码不可空')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_null_all_%s.png' % self.now)

	def test_null_username(self):
		u"""用户名为空"""
		try:
			self.browser.type_username(self.username[2])
			self.browser.type_password(self.password[2])
			self.browser.type_security(self.security[2])
			self.logger.info(
				'username, password, security: %s, %s, %s' % (self.username[2], self.password[2], self.security[2]))
			self.browser.login()
			time.sleep(2)
			text = self.driver.find_element(By.CLASS_NAME, 'warn').text
			self.assertEqual(text, u'用户名不可空')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_null_username_%s.png' % self.now)

	def test_null_password(self):
		u"""密码为空"""
		try:
			self.browser.type_username(self.username[3])
			self.browser.type_password(self.password[3])
			self.browser.type_security(self.security[3])
			self.logger.info(
				'username, password, security: %s, %s, %s' % (self.username[3], self.password[3], self.security[3]))
			self.browser.login()
			time.sleep(2)
			text = self.driver.find_element(By.CLASS_NAME, 'warn').text
			self.assertEqual(text, u'密码不可空')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_null_password_%s.png' % self.now)

	def test_null_security(self):
		u"""验证码为空"""
		try:
			self.browser.type_username(self.username[4])
			self.browser.type_password(self.password[4])
			self.browser.type_security(self.security[4])
			self.logger.info(
				'username, password, security: %s, %s, %s' % (self.username[4], self.password[4], self.security[4]))
			self.browser.login()
			time.sleep(2)
			text = self.driver.find_element(By.CLASS_NAME, 'warn').text
			self.assertEqual(text, u'验证码不可空')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_null_security_%s.png' % self.now)

	def test_username_wrong(self):
		u"""用户名不存在"""
		try:
			self.browser.type_username(self.username[5])
			self.browser.type_password(self.password[5])
			self.browser.type_security(self.security[5])
			self.logger.info(
				'username, password, security: %s, %s, %s' % (self.username[5], self.password[5], self.security[5]))
			self.browser.login()
			time.sleep(2)
			text = self.driver.find_element(By.CLASS_NAME, 'warn').text
			self.assertEqual(text, u'无效的登录用户!')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_username_wrong_%s.png' % self.now)

	def test_user_lock(self):
		u"""用户锁定"""
		lock_time = self.data.select('net_sysconfig', ['DATA'], {'NAME': 'manag_safty_LoginTimes'})
		minute = self.data.select('net_sysconfig', ['DATA'], {'NAME': 'manag_safty_UserLockedTimes'})
		self.browser.type_username(self.username[7])
		self.browser.type_password(self.password[7])
		self.logger.info(
			'username, password, security: %s, %s, %s' % (self.username[7], self.password[7], self.security[7]))
		for t in range(int(lock_time), 0, -1):
			try:
				self.browser.type_security(self.security[7])
				self.browser.login()
				time.sleep(2)
				text = self.driver.find_element(By.CLASS_NAME, 'warn').text
				if t == 1:
					self.assertEqual(text, u'当前用户已被锁定，请%s分钟后重试！' % minute)
				else:
					self.assertEqual(text, u'密码错误!您还有%s次机会。' % (t - 1))
			except Exception as msg:
				self.logger.warning("assert failed: %s" % msg)
				self.driver.get_screenshot_as_file(
					'../images/test_user_lock_%s.png' % self.now)
		service_url = conf['service_url'] + 'UUMSystemService?wsdl'
		client = Client(service_url)
		param = {'userId': 19, 'state': 0}
		client.service.uumUserStateUpdate(**param)

	def test_z_success_login(self):
		u"""登录成功"""
		try:
			self.browser.type_username(self.username[8])
			self.browser.type_password(self.password[8])
			self.browser.type_security(self.security[8])
			self.logger.info(
				'username, password, security: %s, %s, %s' % (self.username[8], self.password[8], self.security[8]))
			self.browser.login()
			time.sleep(2)
			text = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/ul[1]/li[1]/a/span").text
			self.assertEqual(text, u'安全监控')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_z_success_login_%s.png' % self.now)

	def test_z_success_logout(self):
		u"""成功登出"""
		try:
			self.browser.find_element(By.XPATH, '//*[@id="navbar"]/ul[2]/li[5]/img').click()
			text = self.driver.find_element(By.CLASS_NAME, "login-tooltip").text
			self.assertEqual(text, u'欢迎登录')
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(
				'../images/test_z_success_logout_%s.png' % self.now)

	@classmethod
	def tearDownClass(cls):
		cls.browser.close()
		cls.data.close()
