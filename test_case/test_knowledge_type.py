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
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_name_%s.png' % self.now)
			raise

	def test_add_repeat_name(self):
		u"""测试添加已有知识库分类名称"""
		self.logger.info('test add repeat name')
		name = self.name[3]
		try:
			time.sleep(1)
			self.browser.add_press()
			self.browser.type_name(name)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'重复的类别名称!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_repeat_name_%s.png' % self.now)
			raise

	def test_add_child_type(self):
		u"""测试添加知识库分类子类"""
		self.logger.info('test_add_repeat_name')
		name = self.name[5]
		des = self.description[5]
		parent_type = self.parent_type[5]
		try:
			self.browser.add_press()
			time.sleep(1)
			self.browser.type_name(name)
			self.browser.description(des)
			self.browser.choose_father_type(parent_type)
			self.browser.sure_press()
			text = self.browser.get_label()
			id = self.data.select(self.tablename, fields=['type_id'], where_dic={'type_name': name})
			self.assertEqual(u'知识库分类', text)
			if str(id).isdigit():
				pass
			else:
				raise AssertionError('add child knowledge type failed')
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_child_type_%s.png' % self.now)
			raise

	def test_update_repeat(self):
		u"""测试修改成已有知识库分类"""
		self.logger.info('test_update_repeat')
		name = self.name[6]
		try:
			time.sleep(1)
			self.browser.update_press(1)
			self.browser.type_name(name)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'重复的类别名称!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_update_repeat_%s.png' % self.now)
			raise

	def test_update_success(self):
		u"""测试成功修改知识库分类"""
		self.logger.info('test_update_success')
		name = self.name[7]
		des = self.description[7]
		parent = self.parent_type[7]
		try:
			self.browser.update_press(1)
			self.browser.type_name(name)
			self.browser.description(des)
			self.browser.choose_father_type(parent)
			self.browser.sure_press()
			text = self.browser.get_label()
			self.data.commit()
			id = self.data.select(self.tablename, fields=['parent_id'], where_dic={'type_name': name})
			self.assertEqual(u'知识库分类', text)
			self.assertEqual(10, id)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_update_success_%s.png' % self.now)
			raise

	def test_z_delete_cancel(self):
		u"""测试取消删除"""
		self.logger.info('test_z_delete_cancel')
		count_before = self.data.count(self.tablename)
		try:
			self.browser.delete_press(1)
			time.sleep(1)
			self.browser.cancel_press()
			self.data.commit()
			count_after = self.data.count(self.tablename)
			self.assertEqual(count_after, count_before)
		except Exception as msg:
			self.logger.warning(msg)
			raise

	def test_z_delete_quoted(self):
		u"""测试删除已被引用的分类"""
		self.logger.info('test_z_delete_quoted')
		count = self.data.count(self.tablename)
		try:
			self.browser.delete_press(count)
			text = self.browser.tips()
			self.assertEqual(u'被文章引用的分类不得直接删除!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_z_delete_quoted_%s.png' % self.now)
			raise

	def test_z_delete_parent_type(self):
		u"""测试删除父分类"""
		self.logger.info('test_z_delete_parent_type')
		p_name = self.name[3]
		name = self.name[7]
		try:
			parent_id = self.data.select(self.tablename, fields=['type_id'], where_dic={'type_name': p_name})
			self.data.update(self.tablename, new_dict={'parent_id': parent_id}, where_dict={'type_name': name})
			time.sleep(1)
			self.browser.delete_press(2)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'被引用的分类不得直接删除!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_z_delete_parent_type_%s.png' % self.now)
			raise

	def test_z_delete_success(self):
		u"""测试先删除子分类，再删父分类"""
		self.logger.info('test_z_delete_success')
		try:
			before_count = self.data.count(self.tablename)
			self.browser.delete_press(1)
			self.browser.sure_press()
			self.data.commit()
			after_count = self.data.count(self.tablename)
			self.assertEqual(after_count, before_count - 1)
		except Exception as msg:
			self.logger.warning(msg)
			raise
		self.logger.info('delete parent type')
		try:
			before_count = self.data.count(self.tablename)
			time.sleep(1)
			self.browser.delete_press(1)
			self.browser.sure_press()
			self.data.commit()
			after_count = self.data.count(self.tablename)
			self.assertEqual(after_count, before_count - 1)
		except Exception as msg:
			self.logger.warning(msg)
			raise

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
		# cls.driver.quit()
