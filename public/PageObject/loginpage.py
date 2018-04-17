# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'DorisQian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class LoginPage(Page):
	u"""
	登录页面元素操作封装
	"""

	_username_loc = (By.ID, 'txtUserName')
	_password_loc = (By.ID, 'txtPassword')
	_security_loc = (By.ID, 'txtSecurityCode')
	_login_button = (By.CLASS_NAME, 'loginbutton')

	def type_username(self, username):
		self.send_keys(*self._username_loc, value=username)

	def type_password(self, password):
		self.send_keys(*self._password_loc, value=password)

	def type_security(self, security):
		self.send_keys(*self._security_loc, value=security)

	def login(self):
		self.find_element(*self._login_button).click()

