# !/usr/bin/env python3
# -*- coding=utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.page import Page
from selenium.webdriver.common.by import By


class KnowledgePage(Page):
	u"""
	知识库页面封装
	"""

	_knowledge = (By.XPATH, '//*[@id="menu"]/li[3]/ul/li[1]/a')
	_label = (By.CLASS_NAME, 'list-title-left')
	_add = (By.XPATH, '//*[@id="divTop"]/div[2]/button[3]')
	_sure = (By.CLASS_NAME, 'jetsen-btn-sure')
	_cancel = (By.CLASS_NAME, 'jetsen-btn-cancel')
	_know = (By.CLASS_NAME, 'jetsen-btn-know')
	_tips = (By.ID, 'jetsen-alert-control-message')
	_title = (By.ID, 'txt_KNOWLEDGE_TITLE')
	_type = (By.ID, 'cbo_KNOWLEDGE_TYPE')
	_keyword = (By.ID, 'txt_KNOWLEDGE_SUMMARY')
	_source = (By.ID, 'KNOWLEDGE_SOURCE')
	_content = (By.ID, 'txt_KNOWLEDGE_CONTENT')
	_page_info = (By.XPATH, '//*[@id="divKnowledgePage"]/div')
	_delete = (By.XPATH, '//*[@id="divTop"]/div[2]/button[1]')
	_query = (By.XPATH, '//*[@id="divTop"]/div[2]/button[2]')
	_detail_title = (By.ID, 'divKnowledgeTitle8')
	_detail_content = (By.ID, 'divKnowledgeContent8')
	_update_comment = (By.XPATH, '//*[@id="divKnowledgeCommentList4"]/div/div[1]/div[2]/a[1]')
	_delete_comment = (By.XPATH, '//*[@id="divKnowledgeCommentList7"]/div/div[1]/div[2]/a[2]')
	_attachment = (By.ID, 'fileAttachment')
	_download = (By.XPATH, '//*[@id="divKnowledgeAttachment5"]/div[2]/a[1]')
	_delete_attachment = (By.XPATH, '//*[@id="divKnowledgeAttachment6"]/div[2]/a[2]')

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
		path = (By.XPATH, '//*[@id="%s"]/td[8]/a/img' % id)
		self.find_element(*path).click()

	def detail_title(self):
		u"""详细中标题展示"""
		text = self.find_element(*self._detail_title).text
		return text

	def detail_content(self):
		u"""详细中内容展示"""
		text = self.find_element(*self._detail_content).text
		return text

	def comment(self, num, comment):
		u"""
		填写评论
		:param num: 每次点击详细，id会变化，按顺序传入数字确定path
		:param comment:评论内容
		:return:
		"""
		path = (By.ID, 'txtKnowledgeComment%s' % num)
		self.send_keys(*path, value=comment)

	def commit(self, num):
		u"""提交评论"""
		path = (By.XPATH, '//*[@id="divKnowledgeComment%s"]/div/input[1]' % num)
		self.find_element(*path).click()

	def clear(self, num):
		u"""清空评论"""
		path = (By.XPATH, '//*[@id="divKnowledgeComment%s"]/div/input[2]' % num)
		self.find_element(*path).click()

	def get_comment(self, num):
		u"""
		获取文本框中评论内容
		:param num: 传入num来匹配变化的path
		:return:
		"""
		path = (By.ID, 'txtKnowledgeComment%s' % num)
		text = self.find_element(path).text
		return text

	def get_comment_content(self, num, id):
		u"""获取已发表评论内容"""
		_comment_content = (By.ID, 'commentBody%s_%s' % (num, id))
		text = self.find_element(*_comment_content).text
		return text

	def update_comment(self):
		u"""修改评论"""
		self.find_element(*self._update_comment).click()

	def update_content(self, num, content):
		u"""修改评论内容"""
		_update_content = (By.ID, 'txtEditKnowledgeComment%s' % num)
		self.send_keys(*_update_content, value=content)

	def update_commit(self, id):
		u"""提交修改后评论"""
		_update_commit = (By.XPATH, '//*[@id="commentBody4_%s"]/div/input[1]' % id)
		self.find_element(*_update_commit).click()

	def delete_comment(self):
		u"""删除评论"""
		self.find_element(*self._delete_comment).click()

	def multiple_choice(self, source_id, target_id):
		u"""拖拽多选"""
		source_path = (By.XPATH, '//*[@id="%s"]/td[1]' % source_id)
		target_path = (By.XPATH, '//*[@id="%s"]/td[1]' % target_id)
		source = self.find_element(*source_path)
		target = self.find_element(*target_path)
		self.drag_and_drop(source, target)

	def upload(self, id, file):
		u"""
		点击上传,并选择文件
		:param id: 用于定位到上传按钮的xpath
		:param file: 上传文件的绝对路径
		:return:
		"""
		path = '//*[@id="%s"]/td[9]/img' % id
		self.find_element(By.XPATH, path).click()
		self.send_keys(*self._attachment, value=file, clear_first=False, click_first=False)

	def download(self):
		u"""下载附件"""
		self.find_element(*self._download).click()

	def delete_attachment(self):
		u"""删除附件"""
		self.find_element(*self._delete_attachment).click()
