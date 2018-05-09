# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.knowledgePage import KnowledgePage
from public.PageObject.conpage import ConPage
from public.dataConnect import Database
from public.login import Login
import unittest
import xlrd
import math
import time
import os


class Knowledge(unittest.TestCase):
	u"""测试知识库"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test knowledge')
		cls.k_table = 'bmp_knowledge'
		cls.c_table = 'bmp_knowledgecomment'
		file = os.path.abspath('..') + os.sep + 'conf' + os.sep + 'cases.xlsx'
		data = xlrd.open_workbook(file)
		sheet = data.sheet_by_name(u'知识库')
		cls.title = sheet.col_values(6)
		cls.k_type = sheet.col_values(7)
		cls.keyword = sheet.col_values(8)
		cls.source = sheet.col_values(9)
		cls.content = sheet.col_values(10)
		cls.now = time.strftime('%Y-%m-%d')
		cls.data = Database()
		cls.login = Login()
		cls.login.login()
		cls.con = ConPage()
		cls.browser = KnowledgePage()
		cls.driver = cls.browser.driver
		cls.con.sys_conf()
		cls.driver.implicitly_wait(10)
		cls.con.knowledge()
		cls.driver.implicitly_wait(10)
		cls.browser.knowledge()
		cls.driver.implicitly_wait(10)
		cls.driver.switch_to.frame('iframepage')
		cls.driver.implicitly_wait(10)

	def test_add_null_title(self):
		u"""测试不填写标题添加知识库"""
		self.logger.info('test_null_query')
		try:
			self.browser.add_press()
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'不能为空值', text)
			self.browser.know_press()
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_title_%s.png' % self.now)
			raise

	def test_add_null_content(self):
		u"""测试不填写内容添加知识库"""
		self.logger.info('test add null content')
		title = self.title[2]
		try:
			self.browser.add_press()
			self.browser.type_title(title)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'不能为空值', text)
			self.browser.know_press()
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_content_%s.png' % self.now)
			raise

	def test_add_repeat_title(self):
		u"""测试添加知识库时标题重复"""
		self.logger.info('test add repeat title')
		title = self.title[3]
		content = self.content[3]
		try:
			self.browser.add_press()
			self.browser.type_title(title)
			self.browser.type_content(content)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'重复的标题！', text)
			self.browser.know_press()
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_repeat_title_%s.png' % self.now)
			raise

	def test_add_knowledge_success(self):
		u"""测试成功添加知识库"""
		self.logger.info('test add success')
		title = self.title[4]
		k_type = self.k_type[4]
		keyword = self.keyword[4]
		source = self.source[4]
		content = self.content[4]
		try:
			self.browser.add_press()
			self.browser.type_title(title)
			self.browser.choose_type(k_type)
			self.browser.type_keyword(keyword)
			self.browser.type_source(source)
			self.browser.type_content(content)
			self.browser.sure_press()
			id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
			if str(id).isdigit():
				pass
			else:
				raise AssertionError('add  knowledge failed')
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_success_%s.png' % self.now)
			raise

	def test_detail(self):
		u"""测试详细展示"""
		self.logger.info('test detail')
		title = self.title[4]
		content = self.content[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.detail(id)
			d_title = self.browser.detail_title()
			d_content = self.browser.detail_content()
			self.assertEqual(title, d_title)
			self.assertEqual(content, d_content)
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_detail_%s.png' % self.now)
			raise

	def test_add_z_null_content(self):
		u"""测试评论内容为空"""
		self.logger.info('test add null comment content')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.detail(id)
			self.browser.commit()
			text = self.browser.tips()
			self.assertEqual(u"不能为空值", text)
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_z_null_content_%s.png' % self.now)
			raise

	def test_add_z_clear(self):
		u"""测试清空评论"""
		self.logger.info('test add clear comment')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		comment = self.content[6]
		try:
			self.browser.detail(id)
			self.browser.comment(comment)
			self.browser.clear()
			text = self.browser.get_comment()
			self.assertEqual('null', text)
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_z_clear_%s.png' % self.now)
			raise

	def test_add_z_comment_success(self):
		u"""测试成功添加评论"""
		self.logger.info('test add comment success')
		comment = self.content[7]
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.detail(id)
			self.browser.comment(comment)
			self.browser.commit()
			text = self.browser.get_comment_content()
			self.assertEqual(comment, text)
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_z_comment_success_%s.png' % self.now)
			raise

	def test_update_comment(self):
		u"""测试修改评论"""
		self.logger.info('test update comment')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		comment = self.content[9]
		try:
			self.browser.detail(id)
			self.browser.update_comment()
			self.browser.update_content(comment)
			self.browser.update_commit()
			text = self.browser.get_comment_content()
			self.assertEqual(comment, text)
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_z_comment_success_%s.png' % self.now)
			raise

	def test_delete_comment(self):
		u"""测试删除评论"""
		self.logger.info('test delete comment')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			count_before = self.data.count(self.c_table)
			self.browser.detail(id)
			self.browser.delete_comment()
			self.browser.sure_press()
			self.browser.cancel_press()
			self.data.commit()
			after_count = self.data.count(self.c_table)
			self.assertEqual(after_count, count_before)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_delete_comment_%s.png' % self.now)
			raise

	def test_update_knowledge(self):
		u"""修改知识库"""
		self.logger.info('test update knowledge')
		
	@classmethod
	def tearDownClass(cls):
		cls.data.close()
		cls.driver.close()
