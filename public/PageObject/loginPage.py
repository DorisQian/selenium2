# !/usr/bin/env python3
# -*- coding = utf-8 -*-

__author__ = 'Doris Qian'

from page import page
from selenium.webdriver.common.by import By

url = ''
username_loc = (ByID, "freename")
password_loc = (ByID, "freepassword")
login_button = (ByclassName, "loginBtn")


class LoginPage(page):
    def type_username(self, username):
        page.send_keys(self.username_loc, username)

    def type_password(self, password):
        page.send_keys(self.password_loc, password)

    def login(self):
        page.find_element(self.login_button).click()
