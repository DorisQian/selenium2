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
	_content = {By.ID, 'txt_KNOWLEDGE_CONTENT'}
	_page_info = (By.XPATH, '//*[@id="divKnowledgePage"]/div')
	_delete = {By.XPATH, '//*[@id="divTop"]/div[2]/button[1]'}
	_query = {By.XPATH, '//*[@id="divTop"]/div[2]/button[2]'}
	_detail_title = {By.ID, 'divKnowledgeTitle2'}
	_detail_content = {By.ID, 'divKnowledgeContent2'}
	_comment = {By.ID, 'txtKnowledgeComment2'}
	_commit = {By.XPATH, '//*[@id="divKnowledgeComment2"]/div/input[1]'}
	_clear = {By.XPATH, '//*[@id="divKnowledgeComment2"]/div/input[2]'}
	_comment_content = (By.ID, 'commentBody2_21')
	_update_comment = (By.XPATH, '//*[@id="divKnowledgeCommentList2"]/div[2]/div[1]/div[2]/a[1]')
	_update_content = (By.ID, 'txtEditKnowledgeComment2')
	_update_commit = {By.XPATH, '//*[@id="commentBody2_21"]/div/input[1]'}
	_delete_comment = {By.XPATH, '//*[@id="divKnowledgeCommentList2"]/div/div[1]/div[2]/a[2]'}

	def __init__(self):
		super(KnowledgePage, self).__init__()

	def knowledge(self):
		self.find_element(*self._knowledge).click()

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
		:param value: 传入数字，确定knowledge_id，写入xpath
		:return:
		"""
		path = '//*[@id="%s"]/td[10]/img' % value
		self.find_element(By.XPATH, path).click()

	def delete_press(self, value):
		u"""
		点击删除
		:param value: 传入数字，确定knowledge_id，写入xpath
		:return:
		"""
		path = '//*[@id="%s"]/td[11]/img' % value
		self.find_element(By.XPATH, path).click()

	def type_title(self, name):
		u"""填入标题名称"""
		self.send_keys(*self._title, value=name)

	def type_keyword(self, keyword):
		u"""填入关键字"""
		self.send_keys(*self._keyword, value=keyword)

	def type_source(self, source):
		u"""填入来源"""
		self.send_keys(*self._source, value=source)

	def type_content(self, content):
		u"""填写内容"""
		self.send_keys(*self._content, value=content)

	def page_info(self):
		u"""获取最下方页数信息"""
		text = self.find_element(*self._page_info).text
		return text

	def get_label(self):
		u"""获取页面左上角信息，即知识库"""
		text = self.find_element(*self._label).text
		return text

	def choose_type(self, k_type):
		u"""选择分类"""
		self.find_element(*self._type).click()
		path = (By.LINK_TEXT, u'%s' % k_type)
		self.find_element(*path).click()

	def multiple_delete(self):
		u"""多选删除"""
		self.find_element(*self._delete).click()

	def detail(self, id):
		u"""点击详情"""
		path = {By.XPATH, '//*[@id="%s"]/td[8]/a/img' % id}
		self.find_element(*path).click()

	def detail_title(self):
		u"""详细中标题展示"""
		text = self.find_element(*self._detail_title).text
		return text

	def detail_content(self):
		u"""详细中内容展示"""
		text = self.find_element(*self._detail_content).text
		return text

	def comment(self, comment):
		u"""填写评论"""
		self.send_keys(*self._comment, value=comment)

	def commit(self):
		u"""提交评论"""
		self.find_element(*self._commit).click()

	def clear(self):
		u"""清空评论"""
		self.find_element(*self._clear).click()

	def get_comment(self):
		u"""获取文本框中评论内容"""
		text = self.find_element(*self._comment).text
		return text

	def get_comment_content(self):
		u"""获取已发表评论内容"""
		text = self.find_element(*self._comment_content).text
		return text

	def update_comment(self):
		u"""修改评论"""
		self.find_element(*self._update_comment).click()

	def update_content(self, content):
		u"""修改评论内容"""
		self.send_keys(*self._update_content, value=content)

	def update_commit(self):
		u"""提交修改后评论"""
		self.find_element(*self._update_commit).click()

	def delete_comment(self):
		u"""删除评论"""
		self.find_element(*self._delete_comment).click()
