import os
import sys
sys.path.append("../")
import settings  # 邮件的配置文件
from email import message
from fileinput import filename
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
from imbox import Imbox
import zmail
import shutil
import datetime
import time
import imaplib
import random
import util
import shutil

def emailProcess():

    print("\n\n" + datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + "邮件自动回复已启动")

    sender_qq = settings.sender_qq
    pwd = settings.authorization_code
    server = zmail.server(sender_qq, pwd)
    print('login Success')
    print('-----开始接收并处理邮件-----')
    delete_days_ago = datetime.date.fromtimestamp(time.time() - 30 * 24 * 60 * 60)
    print(f"{delete_days_ago=}")

    # while True:
    #     imap = imaplib.IMAP4_SSL('imap.qq.com')
    #     r, d = imap.login(sender_qq, pwd)
    #     assert r == 'OK', 'login failed'
    #     try:
    #         imap.select('inbox')

    #         result, data = imap.search(None, 'ALL')
    #         # do things with imap
    #     except imap.abort:
    #         continue
    #     imap.logout()

    while True:
        time.sleep(10)
        with Imbox('imap.qq.com', sender_qq, pwd, ssl=True) as imbox:
            # 删除旧邮件
            inbox_messages_before=imbox.messages(date__lt=delete_days_ago)
            print(f"inbox_messages_before={inbox_messages_before}")
            for uid, messages in inbox_messages_before:
                try:
                    title = messages.subject
                    sent_from = messages.sent_from
                    receivedate = time.strftime("%Y%m%d %H:%M:%S", time.strptime(messages.date[0:24], '%a, %d %b %Y %H:%M:%S'))
                    if int(receivedate[:8]) > int(datetime.datetime.strftime(delete_days_ago, r'%Y%m%d')):
                        break
                    print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S'), "删除邮件：",uid, f'在 {receivedate} 收到',sent_from,'的邮件，主题为：',title)
                    imbox.delete(uid)
                except Exception as e:
                    print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + f"Error : {e}\n")
                    print(f"删除邮件：{uid=}, {messages.sent_from=}")
                    imbox.delete(uid)

if __name__ == "__main__":
    emailProcess()
