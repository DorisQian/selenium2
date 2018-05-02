# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import smtplib
import os
import time
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from public.log import log

__author__ = 'Doris'


class SendMail:

    logger = log(os.path.basename(__file__))
    now = time.strftime('%Y-%m-%d')

    def send_mail(self, msg, flag, remote_host):
        host = 'smtp.sina.com'
        mail_user = 'doris_test'
        mail_pwd = 'admin@123'

        sender = 'doris_test@sina.com'
        receiver = '1609047552@qq.com'

        remote = remote_host[0]
        browser = remote_host[1]

        html = '''
                <html><body><h1>测试报告链接</h1><p>link <a href="http://172.17.1.213:8080/job/test_selenium2/测试报告/">report</a>...</p>
                <p><img src="cid:0"></p>
                </body></html>
                '''

        with open(msg, 'rb') as f:
            report = f.read()
        message = MIMEMultipart()
        message.attach(MIMEText(html, 'html', 'utf-8'))
        message.attach(MIMEText(report, 'html', 'utf-8'))
        message['From'] = Header('doris_test@sina.com')
        message['To'] = Header('1609047552@qq.com', 'utf-8')
        message['Subject'] = Header(u'测试报告-%s:%s' % (remote, browser), 'utf-8')

        attach = MIMEApplication(open(msg, 'rb').read())
        name = msg.split(os.sep)[-1]
        attach.add_header('Content-Disposition', 'attachment', filename=name)
        message.attach(attach)
        self.logger.info('attach reports')

        # 判断是否有图片打包，发送附件
        if flag == 'over':
            package = os.path.abspath('..') + os.sep + 'images' + os.sep + self.now + '.zip'
            name = remote.split(':')[0] + '-' + browser + self.now + '_image.zip'
            attach = MIMEApplication(open(package, 'rb').read())
            attach.add_header('Content-Disposition', 'attachment', filename=name)
            message.attach(attach)
            self.logger.info('attach images package')

        try:
            server = smtplib.SMTP(host, 25)
            server.login(mail_user, mail_pwd)
            server.sendmail(sender, receiver, message.as_string())
            self.logger.info('send email to %s successful' % receiver)
            server.close()
        except smtplib.SMTPException:
            self.logger.error('send email failed')
            server.close()

    def send_report(self, path, flag, host):
        reports = os.listdir(path)
        reports.sort(key=lambda fn: os.path.getmtime(path+fn))
        self.logger.info('the newest report is %s' % reports[-1])
        file = os.path.join(path, reports[-1])
        self.logger.info('preparing send report %s' % file)
        host = host
        self.send_mail(file, flag, host)

    def pack_images(self):
        img_path = os.path.abspath('..') + os.sep + 'images' + os.sep
        images = os.listdir(img_path)
        images_list = list(images)
        for img in images:
            if not img.endswith('%s.png' % self.now):
                images_list.remove(img)
        if len(images_list) == 0:
            self.logger.info('none of wrong images')
            return 'none'

        else:
            folder = img_path + self.now
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.mkdir(folder)
            for i in images_list:
                src = img_path + i
                shutil.move(src, folder)
            shutil.make_archive(folder, 'zip', root_dir=folder)
            self.logger.info('successful zip to %s.zip' % folder)
            shutil.rmtree(folder)
            return 'over'
