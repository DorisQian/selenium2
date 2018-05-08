# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class KnowledgePage(Page):
	u"""
	知识库页面封装
	"""

	_knowledge = (By.LINK_TEXT, u' 知识库')
	_label = (By.CLASS_NAME, 'list-title-left')
	_add = (By.XPATH, '//*[@id="divTop"]/div[2]/button[3]')
	_sure = (By.CLASS_NAME, 'jetsen-btn-sure')
	_cancel = (By.CLASS_NAME, 'jetsen-btn-cancel')
	_know = (By.CLASS_NAME, 'jetsen-btn-know')
	_tips = (By.ID, 'jetsen-alert-control-message')
	_title = (By.ID, 'txt_KNOWLEDGE_TITLE')
	_type = (By.ID, 'cbo_KNOWLEDGE_TYPE')
	_keyword = (By.ID, 'txt_KNOWLEDGE_SUMMARY')
	_source = {By.ID, 'KNOWLEDGE_SOURCE'}
	_page_info = (By.XPATH, '//*[@id="divKnowledgePage"]/div')
	_delete = {By.XPATH, '//*[@id="divTop"]/div[2]/button[1]'}
	_query = {By.XPATH, '//*[@id="divTop"]/div[2]/button[2]'}

	def __init__(self):
		super(KnowledgePage, self).__init__()

	def knowledge_type(self):
		self.find_element(*self._knowledge_type).click()

	def add_press(self):
		u"""点击添加"""
		self.find_element(*self._add).click()

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
		path = '//*[@id="tabKnowledgeType"]/tbody/tr[%s]/td[4]/a/img' % value
		self.find_element(By.XPATH, path).click()

	def delete_press(self, value):
		u"""
		点击删除
		:param value: 传入数字，确定是第几行，写入xpath
		:return:
		"""
		path = '//*[@id="tabKnowledgeType"]/tbody/tr[%s]/td[5]/img' % value
		self.find_element(By.XPATH, path).click()

	def type_name(self, name):
		u"""添加关注名称"""
		self.send_keys(*self._name, value=name)

	def description(self, description):
		u"""填写描述"""
		self.send_keys(*self._description, value=description)

	def page_info(self):
		u"""获取最下方页数信息"""
		text = self.find_element(*self._page_info).text
		return text

	def get_label(self):
		u"""获取页面左上角信息，即重点关注"""
		text = self.find_element(*self._label).text
		return text

	def choose_father_type(self, father):
		u"""选择父类别"""
		path = (By.LINK_TEXT, u'%s' % father)
		self.find_element(*self._father_type).click()
		self.find_element(*path).click()
