# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.log import log
from public.PageObject.conpage import ConPage
from public.PageObject.manufacturerPage import ManufacturerPage
from public.dataConnect import Database
from public.login import Login
import unittest
import xlrd
import math
import time
import os


class Manufacturer(unittest.TestCase):
	u"""测试厂商管理"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test manufacturer')
		cls.tablename = 'bmp_manufacturers'
		cls.now = time.strftime('%Y-%m-%d')
		file = os.path.abspath('..') + os.sep + 'conf' + os.sep + 'cases.xlsx'
		data = xlrd.open_workbook(file)
		sheet = data.sheet_by_name(u'厂商管理')
		cls.name = sheet.col_values(6)
		cls.description = sheet.col_values(7)
		cls.model = sheet.col_values(8)
		cls.data = Database()
		cls.login = Login()
		cls.login.login()
		cls.con = ConPage()
		cls.browser = ManufacturerPage()
		cls.driver = cls.browser.driver
		cls.con.sys_conf()
		cls.driver.implicitly_wait(10)
		cls.con.function_conf()
		cls.driver.implicitly_wait(10)
		cls.browser.manufacturer()
		cls.driver.implicitly_wait(10)
		cls.driver.switch_to.frame('iframepage')
		cls.driver.implicitly_wait(10)

	def test_null_query(self):
		u"""测试查询条件为空时查询"""
		self.logger.info('test_null_query')
		records = self.data.count(self.tablename)
		page = math.ceil(records / 20)
		self.browser.search()
		time.sleep(1)
		judge = '一共%s页,共%s条记录' % (page, records)
		text = self.browser.page_info()
		self.assertEqual(text, judge)

	def test_turn_page(self):
		u"""测试顺序翻页"""
		self.logger.info('test_turn_page_order')
		records = self.data.count(self.tablename)
		page = math.ceil(records / 20)
		# 顺序向后翻页
		for p in range(page):
			judge = []
			for n in range(1, page + 1):
				# time.sleep(1)
				#style = WebDriverWait(self.driver, 30).until(
					#EC.presence_of_element_located((By.XPATH, '//*[@id="divManPage"]/span[%s]' % n))).get_attribute('style')
				style = self.browser.getattribute(n)
				if style:
					judge.append('1')
				else:
					judge.append('0')
			for j in range(len(judge)):
				try:
					if j == p:
						self.assertEqual(judge[j], '1')
					else:
						self.assertEqual(judge[j], '0')
				except Exception as msg:
					self.logger.info(msg)
					self.driver.get_screenshot_as_file(
						u'../images/manufacturer_顺序向后翻页第%s页_%s.png' % (j + 1, self.now))
					raise
			mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='%s, 1' % ((p + 1) * 20 - 20))
			ui_model = self.browser.get_model(1)
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(ui_model, mysql_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
			if p != page - 1:
				time.sleep(1)
				self.browser.next_page()

		# 顺序向前翻页
		for p in range(page, 0, -1):
			judge = []
			for n in range(page, 0, -1):
				style = self.browser.getattribute(n)
				if style:
					judge.append('1')
				else:
					judge.append('0')
			judge.reverse()
			for j in range(len(judge), 0, -1):
				try:
					if j == p:
						self.assertEqual(judge[j - 1], '1')
					else:
						self.assertEqual(judge[j - 1], '0')
				except Exception as msg:
					self.logger.info(msg)
					self.driver.get_screenshot_as_file(
						u'../images/manufacturer_顺序向前翻页，第%s页_%s.png' % (j, self.now))
					raise
			mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='%s, 1' % (p * 20 - 20))
			ui_model = self.browser.get_model(1)
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(mysql_model, ui_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
			if p != 1:
				self.browser.previous_page()

		# 跳转翻页 + 第一页最后一页
		if page > 1:
			self.browser.turn_page(2)
			mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='20, 1')
			ui_model = self.browser.get_model(1)
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(ui_model, mysql_model)
			except Exception as msg:
				self.logger.error(msg)
				self.driver.get_screenshot_as_file(
					u'../images/manufacturer_跳转到第二页_%s.png' % self.now)
				raise

			self.browser.first_page()
			mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='1')
			ui_model = self.browser.get_model(1)
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(mysql_model, ui_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
		self.browser.last_page()  # 跳转到最后一页
		mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='%s, 1' % (page * 20 - 20))
		ui_model = self.browser.get_model(1)
		if ui_model == ' ':
			ui_model = None
		try:
			self.assertEqual(ui_model, mysql_model)
		except Exception as msg:
			self.logger.error(msg)
			raise
		self.browser.first_page()  # 跳转到第一页
		mysql_model = self.data.select(self.tablename, ['FIELD_1'], limit='1')
		ui_model = self.browser.get_model(1)
		if ui_model == ' ':
			ui_model = None
		try:
			self.assertEqual(ui_model, mysql_model)
		except Exception as msg:
			self.logger.error(msg)
			raise

	def test_add_null_name(self):
		u"""测试添加厂商名称和型号为空"""
		self.logger.info('test_add_null_name')
		self.browser.add_press()
		text = self.browser.windows_label()
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_name_%s.png' % self.now)
			raise
		# 型号
		try:
			self.browser.save_add()
			alert = self.browser.tips()
			self.assertEqual(u'设备型号不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_model_add&save_%s.png' % self.now)
			raise
		try:
			self.browser.sure_press()
			alert = self.browser.tips()
			self.assertEqual(u'设备型号不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_model_save_%s.png' % self.now)
			raise
		# 厂商
		self.browser.data_type()
		try:
			self.browser.save_add()
			alert = self.browser.tips()
			self.assertEqual(u'厂商名称不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_add&save_%s.png' % self.now)
			raise
		try:
			self.browser.sure_press()
			alert = self.browser.tips()
			self.assertEqual(u'厂商名称不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_save_%s.png' % self.now)
			raise
		# 描述
		name = self.name[10]
		time.sleep(1)
		try:
			self.browser.type_name(name)
			self.browser.save_add()
			alert = self.browser.tips()
			self.assertEqual(u'描述不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_des_add&save_%s.png' % self.now)
			raise
		try:
			self.browser.sure_press()
			alert = self.browser.tips()
			self.assertEqual(u'描述不能为空！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_des_save_%s.png' % self.now)
			raise
		self.browser.cancel_press()

	def test_add_repeat_model(self):
		u"""测试添加重复型号"""
		self.logger.info('test_add_repeat_model')
		model = self.model[11]
		self.browser.add_press()
		self.browser.type_model(model)
		self.browser.sure_press()
		alert = self.browser.tips()
		try:
			self.assertEqual(u'设备型号不能重复！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_repeat_model_%s.png' % self.now)
			raise
		self.browser.cancel_press()

	def test_add_success_manu(self):
		u"""测试成功添加厂商"""
		self.logger.info('test_add_success_manu')
		self.browser.add_press()
		# 保存并添加
		self.browser.data_type()
		name = self.name[14]
		description = self.description[14]
		self.browser.type_name(name)
		self.browser.description(description)
		self.browser.save_add()
		text = self.browser.windows_label()
		self.data.commit()
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_add&save_s_%s.png' % self.now)
			raise
		# 添加
		self.browser.data_type()
		name = self.name[21]
		description = self.description[21]
		self.browser.type_name(name)
		self.browser.description(description)
		self.browser.sure_press()
		text = self.browser.get_label()
		self.data.commit()
		try:
			self.assertEqual(u'厂商管理', text)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/manu_add_s_%s.png' % self.now)
			raise

	def test_add_success_model(self):
		u"""测试成功添加型号"""
		self.logger.info('test_add_success_model')
		self.browser.add_press()
		# 保存并添加
		model = self.model[14]
		self.browser.type_model(model)
		self.browser.save_add()
		text = self.browser.windows_label()
		self.data.commit()
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/model_add&save_s_%s.png' % self.now)
			raise
		# 添加
		# time.sleep(1)
		model = self.model[21]
		self.browser.type_model(model)
		self.browser.sure_press()
		text = self.browser.get_label()
		self.data.commit()
		try:
			self.assertEqual(u'厂商管理', text)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/model_add_s_%s.png' % self.now)
			raise

	def test_update_repeat_model(self):
		u"""测试修改型号相同"""
		self.logger.info('test_update_repeat_model')
		time.sleep(1)
		self.browser.update_press(value=1)
		model = self.model[16]
		self.browser.type_model(model)
		self.browser.sure_press()
		alert = self.browser.tips()
		try:
			self.assertEqual(u'设备型号不能重复！', alert)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/model_add_s_%s.png' % self.now)
			raise
		self.browser.cancel_press()

	def test_update_success(self):
		u"""测试修改成功"""
		# 修改厂商名称和描述
		self.logger.info('test_update_success')
		records = self.data.count(self.tablename)
		page = math.ceil(records / 20)
		count = records - 20 * (page - 1) - 3
		limit = records - 4
		self.browser.last_page()
		time.sleep(2)
		self.browser.update_press(count)
		self.browser.data_type()
		name = self.name[17]
		description = self.description[17]
		self.browser.type_name(name)
		self.browser.description(description)
		self.browser.sure_press()
		time.sleep(1)
		manu_name = self.browser.get_name(count)
		manu_des = self.browser.get_desc(count)
		self.data.commit()
		manu_sql = self.data.select(self.tablename, fields=['MAN_NAME'], limit='%s, 1' % limit)
		des_sql = self.data.select(self.tablename, fields=['MAN_DESC'], limit='%s, 1' % limit)
		try:
			self.assertEqual(manu_sql, manu_name)
			self.assertEqual(des_sql, manu_des)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/manu_update_%s.png' % self.now)
			raise
		# 修改产品型号（为空时）
		self.browser.update_press(count)
		self.browser.obj_type()
		model = self.model[17]
		time.sleep(1)
		self.browser.type_model(model)
		self.browser.sure_press()
		time.sleep(1)
		model = self.browser.get_model(count)
		self.data.commit()
		model_sql = self.data.select('bmp_manufacturers', fields=['FIELD_1'], limit='%s, 1' % limit)
		try:
			self.assertEqual(model_sql, model)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/null_model_update_%s.png' % self.now)
			raise
		# 修改产品型号（已有试）
		self.browser.update_press(count + 2)
		self.browser.obj_type()
		model = self.model[22]
		self.browser.type_model(model)
		self.browser.sure_press()
		time.sleep(1)
		model = self.browser.get_model(count + 2)
		self.data.commit()
		model_sql = self.data.select(self.tablename, fields=['FIELD_1'], limit='%s, 1' % (limit + 2))
		try:
			self.assertEqual(model_sql, model)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/model_update_%s.png' % self.now)
			raise

	def test_z_delete_cancel(self):
		u"""测试取消删除"""
		self.logger.info('test_z_delete_cancel')
		records = self.data.count(self.tablename)
		time.sleep(1)
		self.browser.delete_press(1)
		self.browser.cancel_press()
		self.data.commit()
		records_after = self.data.count(self.tablename)
		try:
			self.assertEqual(records, records_after)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			raise

	def test_z_delete_success(self):
		u"""测试成功删除厂商"""
		self.logger.info('test_z_delete_success')

		self.browser.last_page()
		time.sleep(1)
		self.data.commit()
		records = self.data.count(self.tablename)
		page = math.ceil(records / 20)
		count = records - 20 * (page - 1) - 3
		self.browser.delete_press(count)
		self.browser.sure_press()
		time.sleep(1)
		self.data.commit()
		records_after = self.data.count(self.tablename)
		try:
			self.assertEqual(records_after, records - 1)
			self.data.delete(self.tablename, where_dict={'FIELD_1': 'test型号add2'})
			self.data.delete(self.tablename, where_dict={'MAN_NAME': 'test厂商add2'})
			self.data.delete(self.tablename, where_dict={'FIELD_1': 'test型号修改2'})
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			raise

	def test_z_delete_used(self):
		self.logger.info('test_z_delete_used')
		# time.sleep(2)
		self.browser.first_page()  # 跳转到第一页
		time.sleep(1)
		self.browser.delete_press(1)
		text = self.browser.tips()
		try:
			self.assertEqual(u'该厂商下的设备类型已被引用,不能直接删除!', text)
			self.browser.know_press()
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/manu_delete_%s.png' % self.now)
			raise

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		cls.data.close()
