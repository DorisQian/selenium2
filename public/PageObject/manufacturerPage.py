# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class ManufacturerPage(Page):
	u"""
	厂商管理页面封装
	"""
	_manufacturer = (By.LINK_TEXT, u' 厂商管理')
	_label = (By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[1]/label')
	_windows_label = (By.ID, 'new-object-win_title_text')
	_add = (By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button')
	_save_add = (By.CLASS_NAME, 'jetsen-btn-op')
	_search = (By.CLASS_NAME, 'aui-btn-save')
	_sure = (By.CLASS_NAME, 'jetsen-btn-sure')
	_cancel = (By.CLASS_NAME, 'jetsen-btn-cancel')
	_know = (By.CLASS_NAME, 'jetsen-btn-know')
	_tips = (By.ID, 'jetsen-alert-control-message')
	_data_type = (By.ID, 'txt_DATA_TYPE')
	_name = (By.ID, 'txt_MAN_NAME')
	_model_name = (By.ID, 'txt_MAN_KIND')
	_description = (By.ID, 'txt_MAN_DESC')
	_obj_type = (By.ID, 'assetType')
	_page_info = (By.XPATH, '//*[@id="divManPage"]/div')
	_data_manu = (By.XPATH, '//*[@id="txt_DATA_TYPE"]/option[1]')
	_next_page = (By.XPATH, '//*[@id="divManPage"]/img[3]')
	_previous_page = (By.XPATH, '//*[@id="divManPage"]/img[2]')
	_first_page = (By.XPATH, '//*[@id="divManPage"]/img[1]')
	_last_page = (By.XPATH, '//*[@id="divManPage"]/img[4]')

	def __init__(self):
		super(ManufacturerPage, self).__init__()

	def manufacturer(self):
		self.find_element(*self._manufacturer).click()

	def add_press(self):
		u"""点击添加"""
		self.find_element(*self._add).click()

	def search(self):
		u"""点击查询"""
		self.find_element(*self._search).click()

	def save_add(self):
		u"""保存并添加"""
		self.find_element(*self._save_add).click()

	def sure_press(self):
		u"""点击确定"""
		self.find_element(*self._sure).click()

	def cancel_press(self):
		u"""点击取消"""
		self.find_element(*self._cancel).click()

	def know_press(self):
		u"""点击知道了"""
		self.find_element(*self._know).click()

	def tips(self):
		u"""获取提示信息"""
		text = self.find_element(*self._tips).text
		return text

	def update_press(self, value):
		u"""
		点击更新
		:param value: 传入数字，确定是第几行，写入xpath
		:return:
		"""
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[4]/a/img' % value
		self.find_element(By.XPATH, path).click()

	def delete_press(self, value):
		u"""
		点击删除
		:param value: 传入数字，确定是第几行，写入xpath
		:return:
		"""
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[5]/img' % value
		self.find_element(By.XPATH, path).click()

	def type_name(self, name):
		u"""添加厂商名称"""
		self.send_keys(*self._name, value=name)

	def type_model(self, model):
		u"""填写型号名称"""
		self.send_keys(*self._model_name, value=model)

	def page_info(self):
		u"""获取最下方页数信息"""
		text = self.find_element(*self._page_info).text
		return text

	def get_label(self):
		u"""获取页面左上角信息，即厂商管理"""
		text = self.find_element(*self._label).text
		return text

	def windows_label(self):
		u"""获取弹出窗口标签"""
		text = self.find_element(*self._windows_label).text
		return text

	def data_type(self):
		u"""切换基础数据类型-厂商"""
		self.find_element(*self._data_type).click()
		self.find_element(*self._data_manu).click()

	def description(self, description):
		u"""填写描述"""
		self.send_keys(*self._description, value=description)

	def get_name(self, value):
		u"""
		获取厂商名称
		:param value: 传入数字，确定是第几行，写入xpath
		:return: 厂商名称
		"""
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[1]' % value
		text = self.find_element(By.XPATH, path).text
		return text

	def get_desc(self, value):
		u"""
		获取描述信息
		:param value: 传入数字，确定是第几行，写入xpath
		:return: 描述
		"""
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[2]' % value
		text = self.find_element(By.XPATH, path).text
		return text

	def get_model(self, value):
		u"""
		获取型号
		:param value: 传入数字，确定是第几行，写入xpath
		:return: 型号
		"""
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[3]' % value
		text = self.find_element(By.XPATH, path).text
		return text

	def obj_type(self):
		u"""切换资产类型"""
		self.find_element(*self._obj_type).click()
		self.find_element(*(By.XPATH, '//*[@id="assetType"]/option[1]')).click()

	def getattribute(self, value):
		u"""
		获取元素的attribute
		:param value: 传入数字，确定是第几行，写入xpath
		:return: attribute，是否选中
		"""
		path = '//*[@id="divManPage"]/span[%s]' % value
		attribute = self.find_element(By.XPATH, path).get_attribute('style')
		return attribute

	def next_page(self):
		self.find_element(*self._next_page).click()

	def previous_page(self):
		self.find_element(*self._previous_page).click()

	def first_page(self):
		self.find_element(*self._first_page).click()

	def last_page(self):
		self.find_element(*self._last_page).click()

	def turn_page(self, value):
		u"""
		直接跳转到第vlaue页
		:param value: 传入数字，确定是第几行，写入xpath
		:return:
		"""
		path = '//*[@id="divManPage"]/span[%s]' % value
		self.find_element(By.XPATH, path).click()
