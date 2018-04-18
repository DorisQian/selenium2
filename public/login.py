# !/usr/bin/env python3
# -*- coding = utf-8 -*-

__author__ = 'Doris Qian'

from public.PageObject.loginpage import LoginPage
from public.log import log
import os


class Login:
    """
    登录soc的公共类
    """
    def __init__(self):
        self.logger = log(os.path.basename(__file__))
        self.browser = LoginPage()

    def login(self):
        self.browser.open()
        self.browser.type_username('cfgadmin')
        self.browser.type_password('password')
        self.browser.type_security('abcd')
        self.browser.login()
        self.browser.kick_user()
        self.logger.info('login soc')
