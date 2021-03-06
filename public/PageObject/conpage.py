# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class ConPage(Page):
	u"""系统配置页面封装"""

	def sys_conf(self):
		self.find_element(By.LINK_TEXT, u'系统配置').click()

	def function_conf(self):
		self.driver.switch_to.frame('menu-iframe')
		self.find_element(By.LINK_TEXT, u' 功能配置').click()

	def knowledge(self):
		self.driver.switch_to.frame('menu-iframe')
		self.find_element(By.LINK_TEXT, u' 知识库').click()

	def sys_manage(self):
		self.driver.switch_to.frame('menu-iframe')
		self.find_element(By.LINK_TEXT, u' 系统管理').click()