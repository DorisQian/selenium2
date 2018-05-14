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
import subprocess
import pipes
import time
import os
import winrm


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
			time.sleep(1)
			self.browser.add_press()
			self.browser.type_title(title)
			self.browser.type_keyword(keyword)
			self.browser.type_source(source)
			self.browser.type_content(content)
			self.browser.choose_type(k_type)
			self.browser.sure_press()
			time.sleep(1)
			self.data.commit()
			id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
			print(id)
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
		title = self.title[17]
		content = self.content[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.detail(id)
			d_title = self.browser.detail_title()
			d_content = self.browser.detail_content()
			time.sleep(1)
			self.browser.cancel_press()
			self.assertEqual(title, d_title)
			self.assertEqual(content, d_content)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_detail_%s.png' % self.now)
			raise

	def test_add_z_anull_content(self):
		u"""测试评论内容为空"""
		self.logger.info('test add null comment content')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.detail(id)
			time.sleep(1)
			self.browser.commit(1)
			text = self.browser.tips()
			self.browser.know_press()
			self.browser.cancel_press()
			self.assertEqual(u"不能为空值", text)
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
			time.sleep(1)
			self.browser.comment(2, comment)
			self.browser.clear(2)
			self.browser.commit(2)
			text = self.browser.tips()
			self.browser.know_press()
			self.browser.cancel_press()
			self.assertEqual(u"不能为空值", text)
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
			time.sleep(1)
			self.browser.comment(3, comment)
			self.browser.commit(3)
			time.sleep(1)
			self.data.commit()
			c_id = self.data.select(self.c_table, fields=['comment_id'], where_dic={'comment_content': ('@' + comment + '@')})
			text = self.browser.get_comment_content(3, c_id)
			self.browser.cancel_press()
			time.sleep(1)
			self.assertEqual(comment, text)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_z_comment_success_%s.png' % self.now)
			raise

	def test_b_update_comment(self):
		u"""测试修改评论"""
		self.logger.info('test update comment')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		comment = self.content[9]
		o_comment = self.content[7]
		try:
			self.browser.detail(id)
			self.browser.update_comment()
			self.browser.update_content(4, comment)
			c_id = self.data.select(self.c_table, fields=['comment_id'],
									where_dic={'comment_content': ('@' + o_comment + '@')})
			self.browser.update_commit(c_id)
			time.sleep(1)
			text = self.browser.get_comment_content(4, c_id)
			self.browser.cancel_press()
			self.assertEqual(comment, text)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_b_update_comment_%s.png' % self.now)
			raise

	def test_delete_comment(self):
		u"""测试删除评论"""
		self.logger.info('test delete comment')
		title = self.title[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			count_before = self.data.count(self.c_table)
			self.browser.detail(id)
			time.sleep(1)
			self.browser.delete_comment()
			self.browser.sure_press()
			time.sleep(1)
			self.browser.cancel_press()
			self.data.commit()
			after_count = self.data.count(self.c_table)
			self.assertEqual(after_count, count_before - 1)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_delete_comment_%s.png' % self.now)
			raise

	def test_c_update_repeat_title(self):
		u"""修改知识库标题相同"""
		self.logger.info('test update repeat title')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		title = self.title[16]
		try:
			self.browser.update_press(id)
			self.browser.type_title(title)
			self.browser.sure_press()
			text = self.browser.tips()
			self.assertEqual(u'重复的标题！', text)
			self.browser.know_press()
			self.browser.cancel_press()
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_update_repeat_title_%s.png' % self.now)
			raise

	def test_c_update_success(self):
		u"""测试成功修改知识库"""
		self.logger.info('test update knowledge success')
		title = self.title[4]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		title = self.title[17]
		keyword = self.keyword[17]
		source = self.source[17]
		k_type = self.k_type[17]
		content = self.content[17]
		try:
			self.browser.update_press(id)
			self.browser.type_title(title)
			self.browser.type_keyword(keyword)
			self.browser.type_source(source)
			self.browser.choose_type(k_type)
			self.browser.type_content(content)
			self.browser.sure_press()
			self.data.commit()
			time.sleep(1)
			sql_title = self.data.select(self.k_table, fields=['knowledge_title'], where_dic={'knowledge_id': str(id)})
			self.assertEqual(title, sql_title)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_update_success_%s.png' % self.now)
			raise

	def test_z_delete_one(self):
		u"""测试删除一条记录"""
		self.logger.info('test update knowledge success')
		title = self.title[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			before_count = self.data.count(self.k_table)
			self.data.commit()
			time.sleep(1)
			self.browser.delete_press(id)
			self.browser.sure_press()
			time.sleep(1)
			self.data.commit()
			after_count = self.data.count(self.k_table)
			self.assertEqual(after_count, before_count - 1)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_delete_one_%s.png' % self.now)
			raise

	def test_z_multiple_delete(self):
		u"""测试多选删除"""
		self.logger.info('test multiple delete')
		source_title = self.title[28]
		target_title = self.title[29]
		source_id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': source_title})
		target_id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': target_title})
		try:
			before_count = self.data.count(self.k_table)
			self.browser.multiple_choice(source_id, target_id)
			self.browser.multiple_delete()
			self.browser.sure_press()
			time.sleep(1)
			self.data.commit()
			after_count = self.data.count(self.k_table)
			self.assertEqual(after_count, before_count - 2)
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_multiple_delete_%s.png' % self.now)
			raise

	def test_d_upload(self):
		u"""测试上传附件"""
		self.logger.info('test upload attachment')
		attachment = self.title[13]
		title = self.title[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		try:
			self.browser.upload(id, attachment)
			self.browser.sure_press()
			time.sleep(5)
			self.browser.know_press()
			self.data.commit()
			attachment_id = self.data.select('bmp_knowledgeattachment', fields=['attachment_id'],
											where_dic={'knowledge_id': str(id)})
			if str(attachment_id).isdigit():
				pass
			else:
				raise AssertionError('upload failed')
			path = self.data.select('bmp_knowledgeattachment', fields=['attachment_path'],
									where_dic={'knowledge_id': str(id)})
			ssh_host = 'root@172.17.1.208'
			file = '/opt/socserver/webapps/SOC2.0/' + path
			resp = subprocess.call(['ssh', ssh_host, 'test -e ' + pipes.quote(file)])
			if resp == 0:
				pass
			else:
				raise AssertionError('upload failed, server path does not have the file')
		except Exception as msg:
			self.logger.warning(msg)
			self.driver.get_screenshot_as_file(u'../images/test_upload_%s.png' % self.now)
			raise

	def test_d_z_download(self):
		u"""测试下载附件"""
		self.logger.info('test download attachment')
		title = self.title[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': title})
		file_name = self.title[14]
		try:
			self.browser.detail(id)
			self.browser.download()
			self.browser.cancel_press()
			win = winrm.Session('http://172.17.1.205:5985/wsman', auth=('doris', 'admin@123'))
			r = win.run_cmd(('cd C:\\Users\\doris\\Downloads &'
							'dir'))
			files = r.std_out.decode()
			if file_name in files:
				win.run_cmd('cd C:\\Users\\doris\\Downloads &'
							'rm %s' % file_name)
			else:
				raise AssertionError('download attachment failed')
		except Exception as msg:
			self.logger.warning(msg)
			raise

	def test_delete_attachment(self):
		u"""测试删除附件"""
		self.logger.info('test delete attachment')
		title = self.title[17]
		id = self.data.select(self.k_table, fields=['knowledge_id'], where_dic={'knowledge_title': str(title)})
		path = self.data.select('bmp_knowledgeattachment', fields=['attachment_path'], where_dic={'knowledge_id': str(id)})
		try:
			self.browser.detail(id)
			time.sleep(1)
			self.browser.delete_attachment()
			self.browser.sure_press()
			self.browser.cancel_press()
			time.sleep(1)
			self.data.commit()
			attachment_id = self.data.select('bmp_knowledgeattachment', fields=['attachment_id'],
											where_dic={'knowledge_id': str(id)})
			if str(attachment_id).isdigit():
				raise AssertionError('delete attachment failed')
			ssh_host = 'root@172.17.1.208'
			file = '/opt/socserver/webapps/SOC2.0/' + path
			resp = subprocess.call(['ssh', ssh_host, 'test -e ' + pipes.quote(file)])
			if resp == 0:
				raise AssertionError('delete attachment failed, server path still have the file')
		except Exception as msg:
			self.logger.warning(msg)
			raise

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
		cls.driver.quit()
