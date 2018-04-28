# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.keyattentionPage import KeyAttentionPage
from public.PageObject.conpage import ConPage
from public.dataConnect import Database
from public.login import Login
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import xlrd
import math
import time
import os


class KeyAttention(unittest.TestCase):
	u"""测试重点关注"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test key attention')
		cls.tablename = 'nmp_keyattention'
		file = os.path.abspath('..') + os.sep + 'conf' + os.sep + 'cases.xlsx'
		data = xlrd.open_workbook(file)
		login_sheet = data.sheet_by_name(u'重点关注')
		cls.name = login_sheet.col_values(6)
		cls.virus_type = login_sheet.col_values(7)
		cls.attention_type = login_sheet.col_values(8)
		cls.loophole_level = login_sheet.col_values(9)
		cls.now = time.strftime('%Y-%m-%d')
		cls.data = Database()
		cls.login = Login()
		cls.login.login()
		cls.con = ConPage()
		cls.browser = KeyAttentionPage()
		cls.driver = cls.browser.driver
		cls.con.sys_conf()
		cls.driver.implicitly_wait(10)
		cls.con.function_conf()
		cls.driver.implicitly_wait(10)
		cls.browser.keyattention()
		cls.driver.implicitly_wait(10)
		cls.driver.switch_to.frame('iframepage')
		cls.driver.implicitly_wait(10)

	def test_null_query(self):
		u"""测试查询条件为空时查询"""
		self.logger.info('test_null_query')
		records = self.data.count(self.tablename)
		page = math.ceil(records / 20)
		# time.sleep(1)
		self.browser.search()
		time.sleep(1)
		judge = '一共%s页,共%s条记录' % (page, records)
		text = self.browser.page_info()
		self.assertEqual(text, judge)

	def test_add_null_name(self):
		u"""测试添加重点关注名称为空"""
		self.logger.info('test_add_null_name')
		try:
			self.browser.add_press()
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'重点关注名称不能为空!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/keyattention_nullname_%s.png' % self.now)
			raise

	def test_add_null_type(self):
		u"""测试分类名称为空"""
		self.logger.info('test_add_null_type')
		# 分类名称
		name = self.name[2]
		try:
			self.browser.type_name(name)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'关注分类不能为空!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/keyattention_null_type_%s.png' % self.now)
			raise

	def test_add_null_z_level(self):
		u"""测试漏洞级别为空"""
		self.logger.info('test_add_null_z_level')
		a_type = self.attention_type[3]
		try:
			self.browser.attention_type(a_type)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'漏洞级别不能为空!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/keyattention_nulllevel_%s.png' % self.now)
			raise

	def test_add_repeat(self):
		u"""测试同类型下添加相同名称的关注失败"""
		self.logger.info('test_add_repeat')
		name = self.name[4]
		level = self.loophole_level[4]
		try:
			self.browser.type_name(name)
			self.browser.loophole_level(level)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'同分类下关注名称不能相同!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/keyattention_repeat_add_%s.png' % self.now)
			raise

	def test_add_success(self):
		u"""测试添加重点关注成功"""
		self.logger.info('test_add_repeat')
		name = self.name[6]
		virus_type = self.virus_type[6]
		self.browser.type_name(name)
		self.browser.type_virus_type(virus_type)
		self.browser.sure_press()
		text = self.browser.get_label()
		key_id = self.data.select(self.tablename, fields=['id'], where_dic={'attention_name': name})
		try:
			self.assertEqual(u'重点关注', text)
			if key_id.isdigit():
				pass
			else:
				raise AssertionError('add keyattention failed')
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file('../images/keyattention_add_success_%s.png' % self.now)

	def test_add_cancel(self):
		u"""测试取消添加"""
		self.logger.info('test_add_cancel')
		self.browser.add_press()
		name = self.name[5]
		virus_type = self.virus_type[5]
		a_type = self.attention_type[5]
		level = self.loophole_level[5]
		try:
			self.browser.type_name(name)
			self.browser.type_virus_type(virus_type)
			self.browser.attention_type(a_type)
			self.browser.loophole_level(level)
			self.browser.cancel_press()
			text = self.browser.get_label()
			self.assertEqual(u'重点关注', text)
			key_id = self.data.select('nmp_keyattention', fields=['id'], where_dic={'attention_name': '测试UI添加重点关注'})
			if key_id.isdigit():
				raise AssertionError('add keyattention failed')
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file('../images/keyattention_add_cancel_%s.png' % self.now)

	def test_update_repeat(self):
		u"""测试修改为同类型名称相同"""
		self.logger.info('test_update_repeat')
		name = self.name[11]
		sql_name = self.name[6]
		name_list = self.data.select(self.tablename, fields=['attention_name'])
		print(name_list)
		index = name_list.index(sql_name)
		try:
			self.browser.update_press(index + 1)
			self.browser.type_name(name)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'同分类下关注名称不能相同!', text)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file('../images/keyattention_repeat_up_%s.png' % self.now)
			raise

	def test_update_success(self):
		u"""测试修改成功"""
		self.logger.info('test_update_success')
		name = self.name[12]
		a_type = self.attention_type[12]
		try:
			self.browser.type_name(name)
			self.browser.attention_type(a_type)
			self.browser.sure_press()
			text = self.browser.get_label()
			sql_value = self.data.select(self.tablename, fields=['log_type'], where_dic={'attention_name': name})
			self.assertEqual(u'重点关注', text)
			self.assertEqual('(2,3)', sql_value)
		except Exception as msg:
			self.logger.info(msg)
			self.driver.get_screenshot_as_file('../images/keyattention_up_success_%s.png' % self.now)

	def test_z_delete_cancel(self):
		u"""测试取消删除"""
		self.logger.info('test_z_delete_cancel')
		name = self.name[13]
		name_list = self.data.select(self.tablename, fields=['attention_name'])
		index = name_list.index(name)
		try:
			count_before = self.data.count(self.tablename)
			self.browser.delete_press(index + 1)
			self.browser.cancel_press()
			time.sleep(1)
			count_after = self.data.count(self.tablename)
			self.assertEqual(count_after, count_before)
		except Exception as msg:
			self.logger.warning(msg)

	def test_z_delete_success(self):
		u"""测试删除成功"""
		self.logger.info('test_z_delete_success')
		name = self.name[14]
		name_list = self.data.select(self.tablename, fields=['attention_name'])
		index = name_list.index(name)
		try:
			count_before = self.data.count(self.tablename)
			self.browser.delete_press(index + 1)
			self.browser.sure_press()
			time.sleep(1)
			count_after = self.data.count(self.tablename)
			self.assertEqual(count_after, count_before + 1)
		except Exception as msg:
			self.logger.warning(msg)

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		cls.data.close()
