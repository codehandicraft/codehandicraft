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

from dicesDrawing import dicesDrawing
from charDrawing import charDrawing
from dicesVideo import dicesVideo
from reflexDrawing import reflexDrawing
from shadowDrawing import shadowDrawing


def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

def successMail():
    return

def failedMail(subject, content, attachment):
    return 

def getDicesDrawingPath(fileName) :
    return 'dicesDrawing/input/' + fileName

def getCharsDrawingPath(fileName) :
    return 'charDrawing/input/' + fileName

def getReflexDrawingPath(fileName) :
    return 'reflexDrawing/input/' + fileName

def getShadowDrawingPath(fileName) :
    return 'shadowDrawing/input/' + fileName

def getDicesVideoPath(fileName) :
    return 'dicesVideo/input/' + fileName

def rename(name):
    return datetime.datetime.strftime(datetime.datetime.now(), r'%Y%m%d%H%M%S') + '_'+ name

def diceVideoProcess(msg) :
    print("diceVideoProcess start")
    tips = "todo"
    if msg.attachments:
        for attachment in msg.attachments:
            if attachment['filename'].endswith(('.mp4')):
                with open(attachment['filename'], 'wb') as f:
                    # 保存图片到当前目录
                    f.write(attachment['content'].getvalue())
                    f.close()

                    # 图片根据时间重命名
                    newName = rename(attachment['filename'])
                    print("old=", attachment['filename'], "new=", newName)
                    
                    # 根据名字获取路径
                    dicesDrawingPath = getDicesVideoPath(newName)
                    print(f"dicesDrawingPath={dicesDrawingPath}")

                    # 将图片保存到骰子画输入目录
                    oldpath=attachment['filename']
                    os.system(f'mv \'{oldpath}\' \'{dicesDrawingPath}\'')
                    print(f"mv file {attachment['filename']} !")

                    # 获取骰子画
                    ret = dicesVideo.getDicesVideo(dicesDrawingPath, 0)
                    if (ret[0] == False):
                        break
                    return {
                        'subject':'获取骰子动画成功！',
                        'content_text':f'''获取骰子动画成功，请联系qq：1421204127获取视频\r\n
视频名称为：{newName[:-4] + "_out.mp4"} \r\n
视频信息为：{ret[1]} \r\n
具体教程见：https://www.codehandicraft.com/dicesvideotutorial/ \r\n
演示视频见：todo \r\n
tips：{tips} \r\n
                                        '''
                        # 'attachments':[dicesDrawingPath[:-4] + "_out.mp4"]
                    }
            else :
                pass
            break # 目前只处理第一张图片
    else:
        pass
    return {
                'subject':'获取骰子动画失败！',
                'content_text':f'''请在附件中输入 mp4 格式的视频！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
            }

def diceDrawingProcess(msg) :
    tips = "todo"
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or not msg.body['plain'][0].isdigit():
        dice_num = 100
        tips = "骰子数目未设置或设置错误，已使用默认值100"
    else:
        dice_num = int(msg.body['plain'][0])
        if dice_num < 10 or dice_num > 500:
            dice_num = 100
            tips = "骰子数目范围为[10, 500]，超过范围，已使用默认值100"

    if msg.attachments:
        for attachment in msg.attachments:
            if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')):
                with open(attachment['filename'], 'wb') as f:
                    # 保存图片到当前目录
                    f.write(attachment['content'].getvalue())
                    f.close()

                    # 图片根据时间重命名
                    newName = rename(attachment['filename'])

                    # 根据名字获取路径
                    dicesDrawingPath =  getDicesDrawingPath(newName)

                    # 将图片保存到骰子画输入目录
                    # shutil.move(attachment['filename'],'dicesDrawing/input/')
                    shutil.copyfile(attachment['filename'], dicesDrawingPath)
                    os.remove(attachment['filename'])
                    # print(f"remove file {attachment['filename']} !")

                    # 获取骰子画
                    ret = dicesDrawing.getDicesDrawing(dicesDrawingPath, dice_num)
                    if (ret[0] == False):
                        break
                    return {
                        'subject':'获取骰子画成功！',
                        'content_text':f'''获取骰子画成功，本幅画共需要：\r\n
{ret[1][0]}行 * {ret[1][1]}列 = {ret[1][0]*ret[1][1]}个骰子！\r\n\r\n
共有两个附件，其中.jpg文件为骰子画效果参考图，.xls文件为骰子分布。\r\n\r\n
具体教程见：https://www.codehandicraft.com/dicesdrawingtutorial/ \r\n
演示视频见：todo \r\n
tips：{tips} \r\n
                                        ''',
                        'attachments':[dicesDrawingPath[:-4] + "_out.xls",dicesDrawingPath[:-4] + "_out.jpg"]
                    }
            else :
                pass
            break # 目前只处理第一张图片
    else:
        pass
    return {
                'subject':'获取骰子画失败！',
                'content_text':f'''请在附件中输入jpg或png格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
            }

def charDrawingProcess(msg) :
    failed_mail = {'subject':'获取字符画失败！',
                    'content_text':f'''请在附件中输入jpg或png格式的图片！并输入一行字符（2到10个字符，建议中文）！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0:
        return failed_mail
    else:
        # plain = msg.body['plain'][0]
        plain = msg.body['plain'][0].split('\r\n')
        # re.split(r'\r\n', plain)
        # re.split('\n', plain)
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        chars = plain[0]
        if len(chars) < 2 or len(chars) > 10:
            return failed_mail
        edge = 100
        if len(plain) > 1:
            edge = int(plain[1])
            if edge < 20 or edge > 500:
                edge = 100
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')):
            with open(attachment['filename'], 'wb') as f:
                # 保存图片到当前目录
                f.write(attachment['content'].getvalue())
                f.close()

                # 图片根据时间重命名
                newName = rename(attachment['filename'])

                # 根据名字获取路径
                dicesDrawingPath =  getCharsDrawingPath(newName)

                # 将输入图片保存到对应的输入目录
                oldpath=attachment['filename']
                os.system(f'mv \'{oldpath}\' \'{dicesDrawingPath}\'')
                print(f"mv file {attachment['filename']} !")

                # 获取结果
                ret = charDrawing.getCharDrawing(dicesDrawingPath, chars, edge)
                if (ret[0] == False):
                    break
                return {
                    'subject':'获取字符画成功！',
                    'content_text':f'''获取字符画成功，本幅画共需要：\r\n
{ret[1][0]}行 * {ret[1][1]}列 = {ret[1][0]*ret[1][1]}个文字！\r\n\r\n
共有1个附件，其中.txt文件为字符画文本结果。\r\n\r\n
具体教程见：https://www.codehandicraft.com/charsdrawingtutorial/ \r\n
演示视频见：todo \r\n
tips：{tips} \r\n
                                        ''',
                        'attachments':[dicesDrawingPath[:-4] + "_out.txt"]
                    }
        else :
            pass
        break # 目前只处理第一张图片
    return failed_mail

def reflexDrawingProcess(msg) :
    failed_mail = {'subject':f'获取{msg.subject}失败！',
                    'content_text':f'''请在附件中输入jpg或png格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    ratio = 3
    angle = 270
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        pass
    else:
        # plain = msg.body['plain'][0]
        plain = msg.body['plain'][0].split('\r\n')
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        if len(plain[0]) > 0:
            angle = int(plain[0])
        if angle < 80 or angle > 360:
            angle = 270
        
        if len(plain) > 1 and len(plain[1]) > 0:
            ratio = int(plain[1])
            if ratio < 1 or ratio > 100:
                ratio = 3
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')):
            with open(attachment['filename'], 'wb') as f:
                # 保存图片到当前目录
                f.write(attachment['content'].getvalue())
                f.close()

                # 图片根据时间重命名
                newName = rename(attachment['filename'])

                # 根据名字获取路径
                dicesDrawingPath =  getReflexDrawingPath(newName)

                # 将输入图片保存到对应的输入目录
                oldpath=attachment['filename']
                os.system(f'mv \'{oldpath}\' \'{dicesDrawingPath}\'')
                print(f"mv file {attachment['filename']} !")

                # 获取结果
                ret = reflexDrawing.getReflexDrawing(dicesDrawingPath, angle, ratio)
                if (ret[0] == False):
                    break
                return {
                    'subject':f'获取{msg.subject}成功！',
                    'content_text':f'''获取{msg.subject}成功，本幅画的大小为：\r\n
{ret[1][0]} * {ret[1][1]}\r\n\r\n
共有一个附件，其中.jpg文件为生成的目标图片。\r\n\r\n
具体教程见：https://www.codehandicraft.com/reflexdrawingtutorial/ \r\n
演示视频见：todo \r\n
tips：{tips} \r\n
                                        ''',
                        'attachments':[dicesDrawingPath[:-4] + "_out.jpg"]
                    }
        else :
            pass
        break # 目前只处理第一张图片
    return failed_mail

def shadowDrawingProcess(msg):
    failed_mail = {'subject':f'获取{msg.subject}失败！',
                    'content_text':f'''请在附件中输入jpg或png格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    gradient = 5
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        pass
    else:
        # plain = msg.body['plain'][0]
        plain = msg.body['plain'][0].split('\r\n')
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        if len(plain[0]) > 0:
            gradient = int(plain[0])
        if gradient < 3 or gradient > 15:
            gradient = 5
        
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')):
            with open(attachment['filename'], 'wb') as f:
                # 保存图片到当前目录
                f.write(attachment['content'].getvalue())
                f.close()

                # 图片根据时间重命名
                newName = rename(attachment['filename'])

                # 根据名字获取路径
                dicesDrawingPath =  getShadowDrawingPath(newName)

                # 将输入图片保存到对应的输入目录
                oldpath=attachment['filename']
                os.system(f'mv \'{oldpath}\' \'{dicesDrawingPath}\'')
                print(f"mv file {attachment['filename']} !")

                # 获取结果
                ret = shadowDrawing.getShadowDrawing(dicesDrawingPath, gradient)
                if (ret[0] == False):
                    break
                return {
                    'subject':f'获取{msg.subject}成功！',
                    'content_text':f'''获取{msg.subject}成功：\r\n
共有4个附件，分别为灰度图、灰度图边缘线条、灰度分层图、灰度条。\r\n\r\n
具体教程见：todo \r\n
演示视频见：todo \r\n
tips：{tips} \r\n
                                        ''',
                        'attachments':[dicesDrawingPath[:-4] + "_out.jpg", 
                                       dicesDrawingPath[:-4] + "_color.jpg",
                                       dicesDrawingPath[:-4] + "_gray.jpg",
                                       dicesDrawingPath[:-4] + "_canny.jpg"]
                    }
        else :
            pass
        break # 目前只处理第一张图片
    return failed_mail

def error_mail(error=''):
    return {
                'subject':'获取失败！',
                'content_text':f'''内部系统错误，错误信息[{error}]，请联系qq：1421204127进行处理\r\n''',
            }

def default_mail(error=''):
    return {
                'subject':'获取失败！！自动回复，如有打扰，请忽略',
                'content_text':f'''目前已支持的教学如下：\r\n
******************* 骰子画获取方法 *******************\r\n
主题: 骰子画
收件人: 1421204127@qq.com
附件: jpg或png格式的图片
正文: 
效果演示: https://www.codehandicraft.com/reflexdrawingtutorial/ \r\n\r\n
******************* 字符画获取方法 *******************\r\n
主题: 字符画
收件人: 1421204127@qq.com
附件: jpg或png格式的图片
正文: 
效果演示: https://www.codehandicraft.com/reflexdrawingtutorial/ \r\n
                                        ''',
            }

def emailProcess():

    print("\n\n" + datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + "邮件自动回复已启动")

    sender_qq = settings.sender_qq
    pwd = settings.authorization_code
    server = zmail.server(sender_qq, pwd)
    print('login Success')
    print('-----开始接收并处理邮件-----')

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
        with Imbox('imap.qq.com', sender_qq, pwd, ssl=True) as imbox:
            try:
                unread_mails = imbox.messages(unread=True)
                for uid, messages in unread_mails:
                    # 邮件信息
                    title = messages.subject
                    sent_from = messages.sent_from
                    print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : '), uid, '收到',sent_from,'的邮件，主题为：',title)
                    
                    # 根据标题处理结果，获得回执邮件
                    if messages.subject == "骰子画":
                        mail = diceDrawingProcess(messages)
                    elif messages.subject == "骰子动画":
                        mail = diceVideoProcess(messages)
                    elif messages.subject == "字符画":
                        mail = charDrawingProcess(messages)
                    elif messages.subject == "反射画":
                        mail = reflexDrawingProcess(messages)
                    elif messages.subject == "光影画":
                        mail = shadowDrawingProcess(messages)
                    else:
                        continue

                    # 发送邮件
                    print('start send mail')
                    server.send_mail(sent_from[0]['email'], mail)
                    imbox.mark_seen(uid)
                    print('send Success\n')
            except Exception as e:
                print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + f"Error : {e}\n")
                mail = error_mail(e)
                server.send_mail(sent_from[0]['email'], mail)
                imbox.mark_seen(uid)
                continue
            # break;

if __name__ == "__main__":
    emailProcess()
