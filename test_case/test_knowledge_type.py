# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.knowledge_typePage import KnowledgeTypePage
from public.PageObject.conpage import ConPage
from public.dataConnect import Database
from public.login import Login
import unittest
import xlrd
import math
import time
import os


class KnowledgeType(unittest.TestCase):
	u"""测试知识库分类"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test knowledge type')
		cls.tablename = 'bmp_knowledgetype'
		file = os.path.abspath('..') + os.sep + 'conf' + os.sep + 'cases.xlsx'
		data = xlrd.open_workbook(file)
		sheet = data.sheet_by_name(u'知识库分类')
		cls.name = sheet.col_values(6)
		cls.description = sheet.col_values(7)
		cls.parent_type = sheet.col_values(8)
		cls.now = time.strftime('%Y-%m-%d')
		cls.data = Database()
		cls.login = Login()
		cls.login.login()
		cls.con = ConPage()
		cls.browser = KnowledgeTypePage()
		cls.driver = cls.browser.driver
		cls.con.sys_conf()
		cls.driver.implicitly_wait(10)
		cls.con.knowledge()
		cls.driver.implicitly_wait(10)
		cls.browser.knowledge_type()
		cls.driver.implicitly_wait(10)
		cls.driver.switch_to.frame('iframepage')
		cls.driver.implicitly_wait(10)

	def test_add_null_name(self):
		u"""测试添加知识库分类名称为空"""
		self.logger.info('test_add_null_name')
		try:
			self.browser.add_press()
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'不能为空值', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_name_%s.png' % self.now)
			raise

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
		cls.driver.quit()