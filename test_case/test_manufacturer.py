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


class Manufacturer(unittest.TestCase):
	u"""测试厂商管理"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test manufacturer')
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
			cls.browser.manufacturer()
			cls.driver.implicitly_wait(10)
			cls.driver.switch_to.frame('iframepage')
			cls.driver.implicitly_wait(10)
			text = cls.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[1]/label').text
			assert text == u'厂商管理'
		except Exception as msg:
			cls.logger.warning("assert failed: %s" % msg)
			cls.driver.get_screenshot_as_file(
				'../images/manufacturer_%s.png' % cls.now)
			raise

	def test_null_query(self):
		u"""测试查询条件为空时查询"""
		self.logger.info('test_null_query')
		records = self.data.count('bmp_manufacturers')
		page = math.ceil(records / 20)
		# time.sleep(1)
		self.driver.find_element(By.CLASS_NAME, 'aui-btn-save').click()
		time.sleep(1)
		judge = '一共%s页,共%s条记录' % (page, records)
		text = self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/div').text
		self.assertEqual(text, judge)

	def test_turn_page(self):
		u"""测试顺序翻页"""
		self.logger.info('test_turn_page_order')
		records = self.data.count('bmp_manufacturers')
		page = math.ceil(records / 20)
		# 顺序向后翻页
		for p in range(page):
			judge = []
			for n in range(1, page + 1):
				# time.sleep(1)
				style = WebDriverWait(self.driver, 30).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="divManPage"]/span[%s]' % n))).get_attribute('style')
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
			mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='%s, 1' % ((p + 1) * 20 - 20))
			ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(ui_model, mysql_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
			if p != page - 1:
				time.sleep(1)
				self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[3]').click()

		# 顺序向前翻页
		for p in range(page, 0, -1):
			judge = []
			for n in range(page, 0, -1):
				style = self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/span[%s]' % n).get_attribute('style')
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
			mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='%s, 1' % (p * 20 - 20))
			ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(mysql_model, ui_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
			if p != 1:
				self.driver.find_element(By.XPATH, '// *[ @ id = "divManPage"]/img[2]').click()

		# 跳转翻页 + 第一页最后一页
		if page > 1:
			self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/span[2]').click()
			mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='20, 1')
			ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(ui_model, mysql_model)
			except Exception as msg:
				self.logger.error(msg)
				self.driver.get_screenshot_as_file(
					u'../images/manufacturer_跳转到第二页_%s.png' % self.now)
				raise

			self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[1]').click()  # 跳转到第一页
			mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='1')
			ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
			if ui_model == ' ':
				ui_model = None
			try:
				self.assertEqual(mysql_model, ui_model)
			except Exception as msg:
				self.logger.error(msg)
				raise
		self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[4]').click()  # 跳转到最后一页
		mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='%s, 1' % (page * 20 - 20))
		ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
		if ui_model == ' ':
			ui_model = None
		try:
			self.assertEqual(ui_model, mysql_model)
		except Exception as msg:
			self.logger.error(msg)
			raise
		self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[1]').click()  # 跳转到第一页
		mysql_model = self.data.select('bmp_manufacturers', ['FIELD_1'], limit='1')
		ui_model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[3]').text
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
		self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button').click()
		text = self.driver.find_element(By.ID, 'new-object-win_title_text').text
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_null_name_%s.png' % self.now)
			raise
		# 型号
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-op').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'设备型号不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_model_add&save_%s.png' % self.now)
			raise
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'设备型号不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_model_save_%s.png' % self.now)
			raise
		# 厂商
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]/option[1]').click()
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-op').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'厂商名称不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_add&save_%s.png' % self.now)
			raise
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'厂商名称不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_save_%s.png' % self.now)
			raise
		# 描述
		self.driver.find_element(By.ID, 'txt_MAN_NAME').send_keys('test厂商add1')
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-op').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'描述不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_des_add&save_%s.png' % self.now)
			raise
		try:
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
			alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
			self.assertEqual(u'描述不能为空！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_des_save_%s.png' % self.now)
			raise
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-cancel').click()

	def test_add_repeat_model(self):
		u"""测试添加重复型号"""
		self.logger.info('test_add_repeat_model')
		self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='500')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
		try:
			self.assertEqual(u'设备型号不能重复！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/test_add_repeat_model_%s.png' % self.now)
			raise
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-cancel').click()

	def test_add_success_manu(self):
		u"""测试成功添加厂商"""
		self.logger.info('test_add_success_manu')
		self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button').click()
		# 保存并添加
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]/option[1]').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_NAME'), value='test厂商add1')
		self.browser.send_keys(*(By.ID, 'txt_MAN_DESC'), value='test厂商描述1')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-op').click()
		text = self.driver.find_element(By.ID, 'new-object-win_title_text').text
		self.data.commit()
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/manu_add&save_s_%s.png' % self.now)
			raise
		# 添加
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]/option[1]').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_NAME'), value='test厂商add2')
		self.browser.send_keys(*(By.ID, 'txt_MAN_DESC'), value='test厂商描述2')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		text = self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[1]/label').text
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
		self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button').click()
		# 保存并添加
		self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='test型号add1')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-op').click()
		text = self.driver.find_element(By.ID, 'new-object-win_title_text').text
		self.data.commit()
		try:
			self.assertEqual(u'新建厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/model_add&save_s_%s.png' % self.now)
			raise
		# 添加
		# time.sleep(1)
		self.driver.find_element(By.ID, 'txt_MAN_KIND').send_keys('test型号add2')
		# self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='test型号add2')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		text = self.driver.find_element(By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[1]/label').text
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
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[4]/a/img').click()
		text = self.driver.find_element(By.ID, 'edit-object-win_title_text').text
		try:
			self.assertEqual(u'编辑厂商 ', text)
		except Exception as msg:
			self.logger.error(msg)
			self.driver.get_screenshot_as_file(u'../images/test_update_repeat_model_%s.png' % self.now)
		self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='C00')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		alert = self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert-control-message"]').text
		try:
			self.assertEqual(u'设备型号不能重复！', alert)
			self.driver.find_element(By.XPATH, '//*[@id="jetsen-alert_button"]/input').click()

		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/model_add_s_%s.png' % self.now)
			raise
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-cancel').click()

	def test_update_success(self):
		u"""测试修改成功"""
		# 修改厂商名称和描述
		self.logger.info('test_update_success')
		records = self.data.count('bmp_manufacturers')
		page = math.ceil(records / 20)
		count = records - 20 * (page - 1) - 3
		limit = records - 4
		WebDriverWait(self.driver, 30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="divManPage"]/img[4]'))).click()
		# self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[4]').click()
		time.sleep(2)
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[4]/a/img' % count).click()
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="txt_DATA_TYPE"]/option[1]').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_NAME'), value='test厂商add3')
		self.browser.send_keys(*(By.ID, 'txt_MAN_DESC'), value='test厂商描述3')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		time.sleep(1)
		manu_name = WebDriverWait(self.driver, 30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[1]' % count))).text
		manu_des = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[2]' % count).text
		self.data.commit()
		manu_sql = self.data.select('bmp_manufacturers', fields=['MAN_NAME'], limit='%s, 1' % limit)
		des_sql = self.data.select('bmp_manufacturers', fields=['MAN_DESC'], limit='%s, 1' % limit)
		try:
			self.assertEqual(manu_sql, manu_name)
			self.assertEqual(des_sql, manu_des)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/manu_update_%s.png' % self.now)
			raise
		# 修改产品型号（为空时）
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[4]/a/img' % count).click()
		self.driver.find_element(By.XPATH, '//*[@id="assetType"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="assetType"]/option[1]').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='修改型号test1')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		time.sleep(1)
		model = WebDriverWait(self.driver, 30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[3]' % count))).text
		self.data.commit()
		model_sql = self.data.select('bmp_manufacturers', fields=['FIELD_1'], limit='%s, 1' % limit)
		try:
			self.assertEqual(model_sql, model)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/null_model_update_%s.png' % self.now)
			raise
		# 修改产品型号（已有试）
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[4]/a/img' % (count + 2)).click()
		self.driver.find_element(By.XPATH, '//*[@id="assetType"]').click()
		self.driver.find_element(By.XPATH, '//*[@id="assetType"]/option[1]').click()
		self.browser.send_keys(*(By.ID, 'txt_MAN_KIND'), value='test型号修改2')
		self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-sure').click()
		time.sleep(1)
		model = self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[3]' % (count + 2)).text
		self.data.commit()
		model_sql = self.data.select('bmp_manufacturers', fields=['FIELD_1'], limit='%s, 1' % (limit + 2))
		try:
			self.assertEqual(model_sql, model)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/model_update_%s.png' % self.now)
			raise

	def test_z_delete_cancel(self):
		u"""测试取消删除"""
		self.logger.info('test_z_delete_cancel')
		records = self.data.count('bmp_manufacturers')
		time.sleep(1)
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[5]/img').click()
		self.driver.find_element(By.XPATH, '//*[@id="jetsen-confirm_button"]/input[2]').click()
		self.data.commit()
		records_after = self.data.count('bmp_manufacturers')
		try:
			self.assertEqual(records, records_after)
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			raise

	def test_z_delete_success(self):
		u"""测试成功删除厂商"""
		self.logger.info('test_z_delete_success')
		WebDriverWait(self.driver, 30).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="divManPage"]/img[4]'))).click()
		# self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[4]').click()
		time.sleep(1)
		self.data.commit()
		records = self.data.count('bmp_manufacturers')
		page = math.ceil(records / 20)
		count = records - 20 * (page - 1) - 3
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[%s]/td[5]/img' % count).click()
		self.driver.find_element(By.XPATH, '//*[@id="jetsen-confirm_button"]/input[1]').click()
		time.sleep(1)
		self.data.commit()
		records_after = self.data.count('bmp_manufacturers')
		try:
			self.assertEqual(records_after, records - 1)
			self.data.delete('bmp_manufacturers', where_dict={'FIELD_1': 'test型号add2'})
			self.data.delete('bmp_manufacturers', where_dict={'MAN_NAME': 'test厂商add2'})
			self.data.delete('bmp_manufacturers', where_dict={'FIELD_1': 'test型号修改2'})
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			raise

	def test_z_delete_used(self):
		self.logger.info('test_z_delete_used')
		# time.sleep(2)
		self.driver.find_element(By.XPATH, '//*[@id="divManPage"]/img[1]').click()  # 跳转到第一页
		time.sleep(1)
		self.driver.find_element(By.XPATH, '//*[@id="tabMan"]/tbody/tr[1]/td[5]/img').click()
		text = self.driver.find_element(By.ID, 'jetsen-alert-control-message').text
		try:
			self.assertEqual(u'该厂商下的设备类型已被引用,不能直接删除!', text)
			self.driver.find_element(By.CLASS_NAME, 'jetsen-btn-know').click()
		except Exception as msg:
			self.logger.warning("assert failed: %s" % msg)
			self.driver.get_screenshot_as_file(u'../images/manu_delete_%s.png' % self.now)
			raise

	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()
		cls.data.close()
