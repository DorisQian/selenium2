# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import logging
import logging.handlers
import time
import os
import sys

__author__ = 'Doris Qian'


class Logger():
    """
    日志定义
    """
    def __init__(self, log_level):
        self.log_level = log_level

    def print_log(self, level, message):
        # myapp的初始化工作
        logger = logging.getLogger(os.path.basename(sys.argv[0]))
        logger.setLevel(self.log_level)

        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)
        # 添加TimedRotatingFileHandler
        # 定义一个1天换一次log文件的handler
        # 保留5个旧log文件
        day = time.strftime("%Y-%m-%d")
        filename = "../logs/testing" + day + ".log"
        fh = logging.handlers.TimedRotatingFileHandler(filename, when='D', interval=1, backupCount=5)
        fh.setLevel(logging.INFO)

        # 设置后缀名称，跟strftime的格式一样
        fh.suffix = "%Y-%m-%d.log"

        log_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s [%(filename)s:%(lineno)d]')

        ch.setFormatter(log_format)
        fh.setFormatter(log_format)

        logger.addHandler(ch)
        logger.addHandler(fh)

        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)

    def debug(self, message):
        self.print_log('info', message)

    def info(self, message):
        self.print_log('info', message)

    def warning(self, message):
        self.print_log('warning', message)

    def error(self, message):
        self.print_log('error', message)
'''
if __name__ == '__main__':
    log = Logger('INFO')
    log.info('info msg1000')
    log.debug('debug msg')
    log.warning('warning msg')
    log.error('error msg')
'''