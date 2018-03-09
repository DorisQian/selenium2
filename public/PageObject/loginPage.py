# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from .page import Page
from selenium.webdriver.common.by import By
import time

__author__ = 'Doris Qian'


class LoginPage(Page):
    """
    登录页面
    """
    username_loc = (By.ID, "freename")
    password_loc = (By.ID, "freepassword")
    login_button = (By.CLASS_NAME, "loginBtn")

    def open(self):
        Page.open(self)

    def type_username(self, username):
        # self.find_element(*self.username_loc).send_keys(username)
        self.send_keys(self.username_loc, username)
        time.sleep(2)

    def type_password(self, password):
        self.send_keys(self.password_loc, password)
        time.sleep(1)

    def login(self):
        self.find_element(*self.login_button).click()
