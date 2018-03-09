# !/usr/bin/env python3
# -*- coding = utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.loginPage import LoginPage
from selenium import webdriver
import time
from log import Logger
import logging

log = Logger('INFO')


class Login():
    """
    登录邮箱的公共类
    """
    log.info("login the sina mail...")

    @staticmethod
    def login(driver, username, password):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.type_username(username)
        login_page.type_password(password)
        login_page.login()
        time.sleep(2)
        assert (username == 'doris_test@sina.com'), u"用户名称不匹配，登录失败!"


def main():
    username = 'doris_test@sina.com'
    password = 'admin@123'
    driver = webdriver.Chrome()
    # url = '\\'
    Login().login(driver, username, password)


if __name__ == '__main__':
    main()
