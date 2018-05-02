# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class KeyAttentionPage(Page):
	u"""
	重点关注页面封装
	"""

	_keyattention = (By.LINK_TEXT, u' 重点关注')
	#_label = (By.XPATH, '//*[@id="divListTitle"]/label')
	_label = (By.ID, 'divListTitle')
	_add = (By.XPATH, '//*[@id="divTop"]/table/tbody/tr/td/div[2]/button')
	_search = (By.CLASS_NAME, 'aui-btn-save')
	_sure = (By.CLASS_NAME, 'jetsen-btn-sure')
	_cancel = (By.CLASS_NAME, 'jetsen-btn-cancel')
	_know = (By.CLASS_NAME, 'jetsen-btn-know')
	_tips = (By.ID, 'jetsen-alert-control-message')
	_name = (By.ID, 'keyAttentionName')
	_virus_type = (By.ID, 'virusType')
	_attention_type = (By.ID, 'attentionType')
	_loophole_level = (By.ID, 'loopholeLevel')
	_page_info = (By.XPATH, '//*[@id="divKeyAttentionPage"]/div')

	def __init__(self):
		super(KeyAttentionPage, self).__init__()

	def keyattention(self):
		self.find_element(*self._keyattention).click()

	def add_press(self):
		u"""点击添加"""
		self.find_element(*self._add).click()

	def search(self):
		u"""点击查询"""
		self.find_element(*self._search).click()

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
		path = '//*[@id="tabMan"]/tbody/tr[%s]/td[4]/a' % value
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
		u"""添加关注名称"""
		self.send_keys(*self._name, value=name)

	def type_virus_type(self, virus_type):
		self.send_keys(*self._virus_type, value=virus_type)

	def attention_type(self, attention_type):
		u"""
		选择关注类型
		:param attention_type: 关注类型具体中文
		:return:
		"""
		if attention_type == '流行病毒':
			value = 1
		elif attention_type == '重点病毒':
			value = 2
		elif attention_type == '重点漏洞':
			value = 3
		elif attention_type == '关心资产':
			value = 4
		else:
			raise ValueError(u'关注类型不正确')
		self.find_element(*self._attention_type).click()
		self.find_element(By.XPATH, '//*[@id="attentionType"]/option[%s]' % value).click()

	def loophole_level(self, level):
		u"""
		选择漏洞级别
		:param level: 漏洞级别具体中文
		:return:
		"""
		if level == '信息':
			value = 1
		elif level == '低':
			value = 2
		elif level == '中':
			value = 3
		elif level == '高':
			value = 4
		elif level == '紧急':
			value = 5
		else:
			raise ValueError(u'漏洞级别不正确')
		self.find_element(*self._loophole_level).click()
		self.find_element(By.XPATH, '//*[@id="loopholeLevel"]/option[%s]' % value).click()

	def page_info(self):
		u"""获取最下方页数信息"""
		text = self.find_element(*self._page_info).text
		return text

	def get_label(self):
		u"""获取页面左上角信息，即重点关注"""
		text = self.find_element(*self._label).text
		return text
