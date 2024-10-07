import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
import os
import sys
sys.path.append("../")
import settings  # 邮件的配置文件

import datetime
import time
import util
import importlib

# QQ邮箱配置
imap_server = 'imap.qq.com'
smtp_server = 'smtp.qq.com'
smtp_port = 465
# 账号配置
qq_email = settings.sender_qq
password = settings.authorization_code

# 登录IMAP服务器并处理未读邮件
def process_unread_emails():

    # 登录
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(qq_email, password)
    mail.select('inbox')
    print(f'QQ[{qq_email}] login Success')
    
    print('-----开始接收并处理邮件-----')
    while True:
        result, data = mail.uid('search', None, '(UNSEEN)')
        if result != 'OK':
            print(f"search UNSEEN mail error")
            break
        mail_ids = data[0].split()
        print(f"{len(mail_ids) = }")
        for num in mail_ids:
            result, email_data = mail.uid('fetch', num, '(BODY.PEEK[])')
            if result != 'OK':
                print(f"fetch mail uid={num} error")
                continue
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            
            # 解析邮件内容
            from_addr = email.utils.parseaddr(email_message['From'])[1]
            subject = decode_str(email_message['Subject'])
            body = get_email_body(email_message)
            
            print(f"From: {from_addr}")
            print(f"Subject: {subject}")
            print(f"Body: {body.strip()}\n")
            
            # 处理附件
            attachments = process_attachments(email_message)
            send_reply_email(from_addr, subject, body, attachments)

        break
        print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + 'start sleep 300s')
        time.sleep(300)
    mail.close()
    mail.logout()

# 辅助函数：解码邮件主题
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

# 辅助函数：获取邮件正文
def get_email_body(email_message):
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                return body
    else:
        return email_message.get_payload(decode=True).decode()

# 辅助函数：处理附件
def process_attachments(email_message):
    attachments = []
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get('Content-Disposition') is not None:
                filename = part.get_filename()
                if filename:
                    filepath = os.path.join('attachments', filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    attachments.append({'filename': filename, 'path': filepath})
    return attachments

# 发送回复邮件
def send_reply_email(recipient_email, subject, body, attachments):
    """
        发送带有多个附件和正文的回复邮件

        参数:
        recipient_email (str): 收件人的电子邮件地址
        subject (str): 邮件主题
        body (str): 邮件正文
        attachments (list): 附件文件路径的列表
    """
    sender_email = qq_email
    sender_password = password

    recipient_email = sender_email
    # 创建一个邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    print(f"From: {msg['From']}")
    print(f"To: {msg['To']}")
    print(f"Subject: {subject}")

    # subject = mail['subject']
    # body = mail['content_text']
    # attachments = mail['attachments']

    # 添加邮件正文
    msg.attach(MIMEText(body, 'plain'))

    # 添加附件
    for attachment in attachments:
        print(f"attachment: {attachment}")
        attachment = "temp.txt"
        if os.path.isfile(attachment):
            part = MIMEApplication(open(attachment, 'rb').read(), Name=os.path.basename(attachment))
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment)
            msg.attach(part)
        else:
            print(f"文件 {attachment} 不存在，请检查文件路径。")
        break

    # 连接到SMTP服务器并发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # QQ邮箱SMTP服务器及端口号
        # server.starttls()  # 启动TLS加密
        server.login(sender_email, sender_password)  # 登录到SMTP服务器
        server.sendmail(sender_email, recipient_email, msg.as_string())  # 发送邮件
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")
    finally:
        server.quit()  # 断开与SMTP服务器的连接

def emailProcess():
    print("\n\n" + datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + "邮件自动回复已启动")
    process_unread_emails()

if __name__ == "__main__":
    emailProcess()
