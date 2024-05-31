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
import importlib

from dicesDrawing import dicesDrawing
from charDrawing import charDrawing
from dicesVideo import dicesVideo
from reflexDrawing import reflexDrawing
from shadowDrawing import shadowDrawing
from dragonScaleBinding import dragonScaleBinding
from sketchDrawing import sketchDrawing
from pointDrawing import pointDrawing
from rasterBar import rasterBar

# 定义一个字典，映射输入字符串到对应的子目录中的模块和函数名
SUBJECT_TO_MODULE_FUNCTION= {
    # "光栅卡": ("rasterCard.rasterCard", "getRasterCard"),
    "圆规画": ("circleDrawing.circleDrawing", "getCircleDrawing"),
    # 添加更多的映射
    # "邮件主题": ("子目录.模块名", "函数名"),
}

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
    """
    重命名函数，将当前时间与输入的name拼接后返回新名称
    
    Args:
        name (str): 需要拼接的字符串
    
    Returns:
        str: 拼接后的新名称，格式为 YYYYMMDDHHMMSS_name
    """
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
            if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')) or attachment['filename'].endswith(('.jpeg')):
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
    在正文中可以输入骰子行数，如200，表示使用200行骰子，默认值为100\r\n
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
                'content_text':f'''请在附件中输入jpg、png或jpeg格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
            }

def charDrawingProcess(msg) :
    failed_mail = {'subject':'获取字符画失败！',
                    'content_text':f'''请在附件中输入jpg、png或jpeg格式的图片！并输入一行字符（2到10个字符，建议中文）！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0:
        return failed_mail
    else:
        # plain = msg.body['plain'][0]
        # plain = msg.body['plain'][0].split('\n')
        plain = [string.strip() for string in msg.body['plain'][0].split('\n') if string.strip()]
        
        # re.split(r'\r\n', plain)
        # re.split('\n', plain)
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        chars = plain[0]
        if len(chars) < 2 or len(chars) > 20:
            return failed_mail
        edge = 100
        if len(plain) > 1 and plain[1].isdigit():
            edge = int(plain[1])
            if edge < 20 or edge > 500:
                edge = 100
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')) or attachment['filename'].endswith(('.jpeg')):
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
                        'attachments':[dicesDrawingPath[:-4] + "_out.txt",
                                         dicesDrawingPath[:-4] + "_out.html",
                                        #  dicesDrawingPath[:-4] + "_out.xlsx",
                                         dicesDrawingPath[:-4] + "_out.xls",
                                         ]
                    }
        else :
            pass
        break # 目前只处理第一张图片
    return failed_mail

def reflexDrawingProcess(msg) :
    failed_mail = {'subject':f'获取{msg.subject}失败！',
                    'content_text':f'''请在附件中输入jpg、png或jpeg格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    ratio = 3
    angle = 270
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        pass
    else:
        # plain = msg.body['plain'][0]
        plain = msg.body['plain'][0].split('\r\n')
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        if len(plain[0]) > 0 and plain[0].isdigit():
            angle = int(plain[0])
        if angle < 80 or angle > 360:
            angle = 270
        
        if len(plain) > 1 and len(plain[1]) > 0 and plain[1].isdigit():
            ratio = int(plain[1])
            if ratio < 1 or ratio > 100:
                ratio = 3
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')) or attachment['filename'].endswith(('.jpeg')):
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
                    'content_text':f'''请在附件中输入jpg、png或jpeg格式的图片！\r\n\r\n具体教程见：todo \r\n演示视频见：todo \r\n''',
                    }
    gradient = 5
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        pass
    else:
        # plain = msg.body['plain'][0]
        plain = msg.body['plain'][0].split('\r\n')
        print("msg plain:", msg.body['plain'], "new plain=", plain)
        if len(plain[0]) > 0 and plain[0].isdigit():
            gradient = int(plain[0])
        if gradient < 3 or gradient > 15:
            gradient = 5
        
    tips = "todo"
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.jpg')) or attachment['filename'].endswith(('.jpeg')):
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
                                       dicesDrawingPath[:-4] + "_canny.jpg",
                                       dicesDrawingPath[:-4] + "_canny_under.jpg"]
                    }
        else :
            pass
        break # 目前只处理第一张图片
    return failed_mail

def dragonScaleBindingProcess(msg):
    failed_mail = {'subject':f'获取{msg.subject}失败！',
                    'content_text':f'''请在附件中输入 至少两张 jpg、png或jpeg格式的图片！\r\n
请不要使用 超大附件 发送邮件！！！暂不支持解析超大附件，如果提示使用超大附件，说明图片太大，缩小图片。每张图片一般在1~2M
尽量不要使用png格式，占用的空间较大。可以把封面图片改为jpg格式（直接改） \r\n''',
                    }
    tips_info = '''请不要使用 超大附件 发送邮件！！！暂不支持解析超大附件，如果提示使用超大附件，说明图片太大，缩小图片。每张图片一般在1~2M'''
    other_info = '''具体教程见： 
    B站 : https://b23.tv/gSzDvHg
    抖音 : https://v.douyin.com/ietQup6d/
演示视频见：
    B站 : https://b23.tv/Vg0DEyl
    抖音 : https://v.douyin.com/ieFfGbph/'''
    
    input_file_list = []
    param_int_list = []
    is_use_default_param = False
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        msg.body['plain'][0] = ''
        print("msg plain is empty")
    else:
        # plain = msg.body['plain'][0]
        print("msg plain:", msg.body['plain'])
        plain = msg.body['plain'][0].split('\r\n')
        print("new plain=", plain)
        if len(plain) <= 3:
            plain = plain[0].split('\n')
            print("size=1, use '\\n' split. new plain=", plain)
        if len(plain) <= 3:
            plain = plain[0].split('&nbsp;')
            print("size=1, use '&nbsp;' split. new plain=", plain)
        if len(plain) <= 3:
            plain = plain[0].split(' ')
            print("size=1, use ' ' split. new plain=", plain)

        param_list = plain
        for param in param_list:
            if len(param) == 0:
                continue
            digit = util.str_to_int(param)
            if digit != -1:
                param_int_list.append(int(digit))
            else:
                break

            # if len(param) > 0 and param.isdigit():
            #     param_int_list.append(int(param))
            # elif len(param) == 0:
            #     continue
            # else:
            #     break
        if len(param_int_list) < 4:
            is_use_default_param = True 
            print(f'param num < 4, will use default param')
        
    tips = "todo"

    ts_ms_str = str(int(time.time() * 1000) % 1000) + '_' + str(random.randint(100000, 999999))
    new_dir = f'dragonScaleBinding/input/{rename(ts_ms_str)}/'
    os.system(f'mkdir \'{new_dir}\'')

    file_index = 0
    for attachment in msg.attachments:
        if attachment['filename'].endswith(('.png')) or attachment['filename'].endswith(('.PNG')) or attachment['filename'].endswith(('.jpg')) or attachment['filename'].endswith(('.JPG')) or attachment['filename'].endswith(('.jpeg')):
            with open(attachment['filename'], 'wb') as f:
                oldpath=attachment['filename']

                # 保存图片到当前目录
                f.write(attachment['content'].getvalue())
                f.close()

                # 图片根据时间重命名
                newName = rename(attachment['filename'])

                # 根据名字获取路径
                dicesDrawingPath = new_dir + str(file_index) + os.path.splitext(oldpath)[1]
                file_index += 1
                # 将输入图片保存到对应的输入目录
                shutil.move(oldpath, dicesDrawingPath)
                # os.system(f'mv \'{oldpath}\' \'{dicesDrawingPath}\'')
                print(f"mv file {oldpath} to {dicesDrawingPath} !")
                input_file_list.append(dicesDrawingPath)
        else:
            print(f"fail to parse file: {attachment['filename']}")
            # return failed_mail
            return get_fail_mail(msg, f"不支持该文件格式: {attachment['filename']}，目前支持的文件格式为jpg、png、jpeg", tips_info, other_info)
    if len(input_file_list) < 2:
        print(f'input_file_list = {input_file_list} < 2, will return failed_mail')
        return get_fail_mail(msg, f"附件中的图片个数小于2，请在附件中输入至少两张jpg、png或jpeg格式的图片！", tips_info, other_info)
        # return failed_mail
    # 获取结果
    ret = dragonScaleBinding.getDragonScaleBinding(input_file_list, param_int_list)
    if (ret[0] == False):
        return get_fail_mail(msg, ret[1], tips_info, other_info)
        # return failed_mail
    else:
        img_size_cm = ret[1][0]
        out_path_list = ret[1][1]
        h_w_split_cover = ret[1][2]
        base_path_list = [os.path.basename(path) for path in out_path_list]
        return {
            'subject':f'获取{msg.subject}成功！',
            'content_text':f'''获取{msg.subject}成功：
【重要！！！】有任何问题请先看完下面的tips \r\n
采用的输入参数为：【{h_w_split_cover[0]} {h_w_split_cover[1]} {h_w_split_cover[2]} {h_w_split_cover[3]} {h_w_split_cover[4]} {h_w_split_cover[5]}】
如果与你的输入不一致，可能输入参数有误，使用的是默认参数，请检查输入参数！（一共6个参数，每个参数为正整数，且单独占一行）\r\n
共有{len(base_path_list)}个附件，其中需要打印的图片有{len(base_path_list)-1}张，即『 0_page_img_ 』开头的图片。。。\r\n
需要预留粘贴的卷轴尺寸为：{h_w_split_cover[0]}厘米 * {h_w_split_cover[1]}厘米。。。 \r\n
每张图片的打印尺寸为： {img_size_cm[0]}厘米 * {img_size_cm[1]}厘米 ，打印前请确认尺寸是否正确！！！\r\n
预计成品需要打印纸张{h_w_split_cover[2]-h_w_split_cover[3]}张，其中前后封面会使用2页(一张)。。。\r\n
其中最后一张图片为连成一体的效果预览图：{base_path_list[-1]}。\r\n\r\n
具体教程见：
    B站 : https://b23.tv/gSzDvHg
    抖音 : https://v.douyin.com/ietQup6d/
效果视频见：
    B站 : https://b23.tv/Vg0DEyl
    抖音 : https://v.douyin.com/ieFfGbph/
多多点赞转发支持下吧  \^O^/ 
\r\n
tips：
0、因为成本较高，先简单A4黑白打印前几张图片（手动裁剪白边之后）试试效果，之后再彩色打印进行正式的制作。（主要看误差如何）
1、粘贴时以固体胶为主，白乳胶为辅（空白部分粘贴到卷轴上时需要用少量白乳胶辅助粘贴）
2、成品卷轴卷起来的时候不要太紧，否则对折的纸张可能会有挤压的痕迹
3、最后的裁剪图片以封面图片的清晰度为基准，觉得结果图片清晰度不够的话可以使用微信小程序bigjpg放大（二次元图片）
4、请不要使用 超大附件 发送邮件！！！当前邮件服务接收不到超大附件，如果提示使用超大附件，说明图片太大，缩小图片。每张图片一般在1~2M
5、如果存在空白内容页，说明对应图片的格式或名字不符合要求，请替换
6、每一行参数都需要为整数，暂不支持小数
7、如果有部分内容页为空白，可能是程序无法加载的图片格式，可以把这些图片发送到QQ重新保存一下，再发送过来；也可能是附件图片个数不够
8、如果内容图片被裁剪，是因为正文参数和图片的尺寸不匹配。图方便可以再额外增加两行数字：第五行写0，第六行写1。这样就不会被裁剪了，但会有白边。
9、如果封面图片被裁剪，是前两行参数和图片的尺寸不匹配导致的，请按需修改前两行参数。
10、服务生效时间一般在10-22点
解释下各个参数的意思:
    假设前四行参数各位A、B、C、D，那么封面图片的高宽比=A:B；内容图片的高宽比=A:(2D-1)B/C；其中内容图片的个数=C-D-1
    另外，
    可选的第五行参数为是否单面打印（0或1，默认为0不进行单面打印）；
    可选的第六行参数为内容图片通过切割还是填充空白统一尺寸（0或1，默认为0通过切割进行统一尺寸）。

\r\n
                                ''',
                'attachments':out_path_list
            }

    return failed_mail
    

def get_plain_param(msg):
    '''解析邮件正文参数——整数'''
    param_int_list = []
    if 'plain' not in msg.body or len(msg.body['plain']) <= 0 or msg.body['plain'][0] == '':
        msg.body['plain'][0] = ''
        print("msg plain is empty")
    else:
        # plain = msg.body['plain'][0]
        print("msg plain:", msg.body['plain'])
        plain = msg.body['plain'][0].split('\r\n')
        print("new plain=", plain)
        if len(plain) == 1:
            plain = plain[0].split(' ')
            print("size=1, use ' ' split. new plain=", plain)
        if len(plain) == 1:
            plain = plain[0].split('\n')
            print("size=1, use '\\n' split. new plain=", plain)
        if len(plain) == 1:
            plain = plain[0].split('&nbsp;')
            print("size=1, use '&nbsp;' split. new plain=", plain)

        param_list = plain
        for param in param_list:
            if len(param) > 0 and param.isdigit():
                param_int_list.append(int(param))
            else:
                break
    print(f"get param success: {param_int_list}")
    return param_int_list

def get_img_file(msg, dir_path):
    '''解析邮件附件图片到新的目录中'''
    input_file_list = []
    input_dir = f'{dir_path}/input/'
    if not util.check_directory_exists(input_dir):
        util.create_dir(input_dir)

    # 新建用户目录 
    ts_ms_str = str(int(time.time() * 1000) % 1000) + '_' + str(random.randint(100000, 999999))
    new_dir = f'{dir_path}/input/{rename(ts_ms_str)}/'
    util.create_dir(new_dir)

    # 附件提取到新目录中
    file_index = 0
    for attachment in msg.attachments:
        path_pair = os.path.splitext(attachment['filename'])
        if len(path_pair) > 1 and path_pair[1].lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            with open(attachment['filename'], 'wb') as f:
                # 保存图片到当前目录
                oldpath=attachment['filename']
                f.write(attachment['content'].getvalue())
                f.close()

                # 根据名字获取路径
                dicesDrawingPath = new_dir + str(file_index) + os.path.splitext(oldpath)[1]
                file_index += 1
                # 将输入图片保存到对应的输入目录
                shutil.move(oldpath, dicesDrawingPath)
                print(f"mv file {oldpath} to {dicesDrawingPath} !")
                input_file_list.append(dicesDrawingPath)
        else:
            print(f"fail to parse file: {attachment['filename']}")
            return []
    return input_file_list

def get_fail_mail(msg, fail_reason='', tips_info='无', other_info='无'):
    fail_mail = {'subject':f'获取{msg.subject}失败！(自动发送,请勿回复)',
                    'content_text':f"************* 失败原因 *************\r\n{fail_reason}\r\n\r\n"
                                    f"************* 提示信息 *************\r\n{tips_info}\r\n\r\n"
                                    f"************* 其他信息 *************\r\n{other_info}\r\n\r\n",
                    }
    print(f"{fail_mail=}")
    return fail_mail

def get_succ_mail(msg, in_param_list, out_path_list, other_info=''):
    succ_mail = {
        'subject':f'获取{msg.subject}成功！(自动发送,请勿回复)',
        'content_text':f'''获取{msg.subject}成功：
服务生效时间一般在工作日的10-22点 \r\n
输入参数为{in_param_list}，如果与预期的参数不同，则使用的是默认参数 \r\n
{other_info}
\r\n                ''',
            'attachments':out_path_list
        }
    return succ_mail

def sketchDrawingProcess(msg):
    failed_mail = get_fail_mail(msg)
    
    # 解析参数和输入附件
    param_int_list = get_plain_param(msg)
    input_file_list = get_img_file(msg, 'sketchDrawing')
    if not input_file_list:
        print(f'input_file_list is empty, will return failed_mail')
        return failed_mail

    # 获取结果
    ret = sketchDrawing.getSketchDrawing(input_file_list, param_int_list)
    if (ret[0] == False):
        return failed_mail
        
    # 返回结果
    in_param_list = ret[1]['in_param_list']
    out_path_list = ret[1]['out_path_list']
    base_path_list = [os.path.basename(path) for path in out_path_list]
    return get_succ_mail(msg, in_param_list, out_path_list)

def pointDrawingProcess(msg):
    failed_mail = get_fail_mail(msg)
    
    # 解析参数和输入附件
    param_int_list = get_plain_param(msg)
    input_file_list = get_img_file(msg, 'pointDrawing')
    if not input_file_list:
        print(f'input_file_list is empty, will return failed_mail')
        return failed_mail

    # 获取结果
    ret = pointDrawing.getPointDrawing(input_file_list, param_int_list)
    if (ret[0] == False):
        return failed_mail
        
    # 返回结果
    in_param_list = ret[1]['in_param_list']
    out_path_list = ret[1]['out_path_list']
    base_path_list = [os.path.basename(path) for path in out_path_list]
    return get_succ_mail(msg, in_param_list, out_path_list)

def rasterBarProcess(msg):
    # 解析参数和输入附件
    param_int_list = get_plain_param(msg)
    input_file_list = get_img_file(msg, 'rasterBar')
    if len(input_file_list) <= 1:
        print(f'input_file_list is empty, will return failed_mail')
        return get_fail_mail(msg, '输入图片数量小于2', '至少上传两张图片；图片不要用超大附件发送；图片不要放在正文中')

    # 获取结果
    ret = rasterBar.getRasterBar(input_file_list, param_int_list)
    if (ret[0] == False):
        return get_fail_mail(msg, ret[1])
        
    # 返回结果
    in_param_list = ret[1]['in_param_list']
    out_path_list = ret[1]['out_path_list']
    tip_info = ret[1]['tip_info']
    base_path_list = [os.path.basename(path) for path in out_path_list]
    return get_succ_mail(msg, in_param_list, out_path_list, tip_info)

def subModuleProcess(msg, module_info):
    module_name, function_name = module_info
    # 解析参数和输入附件
    param_int_list = get_plain_param(msg)
    input_file_list = get_img_file(msg, module_name.split('.')[0])

    # 动态导入模块,获取模块中的函数,调用函数并返回结果
    ret = getattr(importlib.import_module(module_name), function_name)(input_file_list, param_int_list)
    if (ret[0] == False):
        return get_fail_mail(msg, ret[1], ret[2])
        
    # 返回结果
    in_param_list = ret[1]['in_param_list']
    out_path_list = ret[1]['out_path_list']
    tip_info = ret[1]['tip_info']
    return get_succ_mail(msg, in_param_list, out_path_list, tip_info)

def error_mail(error=''):
    return {
                'subject':'获取失败！',
                'content_text':f'''内部系统错误，错误信息[{error}]，建议使用qq邮箱发送邮件。请私信博主进行处理\r\n''',
            }

def default_mail(title, error=''):
    return {
                'subject':'获取失败！！自动回复，如有打扰，请忽略',
                'content_text':f'''主题错误：[{title}] 暂不支持\n
''',
# 目前支持的主题有：骰子画、字符画、反射画、光影画 \n
# 骰子画：以 骰子画 为主题，jpg、png或jpeg格式的图片为附件，发送给 1421204127@qq.com \n
# 字符画：以 字符画 为主题，任意一行文本为正文，jpg、png或jpeg格式的图片为附件，发送给 1421204127@qq.com \n
# 反射画：以 反射画 为主题，jpg、png或jpeg格式的图片为附件，发送给 1421204127@qq.com \n
# 光影画：以 光影画 为主题，jpg、png或jpeg格式的图片为附件，发送给 1421204127@qq.com \n
            }
# ******************* 骰子画获取方法 *******************\r\n
# 主题: 骰子画
# 收件人: 1421204127@qq.com
# 附件: jpg、png或jpeg格式的图片
# 正文: 
# 效果演示: https://www.codehandicraft.com/reflexdrawingtutorial/ \r\n\r\n
# ******************* 字符画获取方法 *******************\r\n
# 主题: 字符画
# 收件人: 1421204127@qq.com
# 附件: jpg、png或jpeg格式的图片
# 正文: 
# 效果演示: https://www.codehandicraft.com/reflexdrawingtutorial/ \r\n

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
            try:
                unread_mails = imbox.messages(unread=True)
                for uid, messages in unread_mails:
                    # 邮件信息
                    title = messages.subject
                    sent_from = messages.sent_from
                    if sent_from[0]['email'] == 'dragon_0417@qq.com':
                        sent_from[0]['email'] = '1063068121@qq.com'
                    print("\n====================================================== new email ====================================================== ")
                    print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : '), uid, '收到',sent_from,'的邮件，主题为：',title)
                    print(f"messages: {messages.__dict__.keys()}")

                    # 根据标题处理结果，获得回执邮件
                    is_skip = False
                    for black_word in ['撤回', '回复', '自动', '失败', '成功', '邮箱']:
                        if black_word in title:
                            imbox.mark_seen(uid)
                            print(f'{black_word} in title:{messages.subject}, will skip\n')
                            is_skip = True
                            break
                    if is_skip:
                        continue
                    if "骰子画" in messages.subject:
                        mail = diceDrawingProcess(messages)
                    elif "骰子动画" in messages.subject:
                        mail = diceVideoProcess(messages)
                    elif "字符画" in messages.subject:
                        mail = charDrawingProcess(messages)
                    elif "反射画" in messages.subject:
                        mail = reflexDrawingProcess(messages)
                    elif "光影画" in messages.subject:
                        mail = shadowDrawingProcess(messages)
                    elif "龙鳞" in messages.subject or "龙麟" in messages.subject:
                        mail = dragonScaleBindingProcess(messages)
                    elif "线稿" in messages.subject:
                        mail = sketchDrawingProcess(messages)
                    elif "点画" in messages.subject:
                        mail = pointDrawingProcess(messages)
                    elif "光栅条" in messages.subject or "光栅画" in messages.subject or "光栅图" in messages.subject:
                        mail = rasterBarProcess(messages)
                    elif messages.subject in SUBJECT_TO_MODULE_FUNCTION:
                        mail = subModuleProcess(messages, SUBJECT_TO_MODULE_FUNCTION[messages.subject])
                    else:
                        mail = default_mail(messages.subject)

                    # 发送邮件
                    print('start send mail')
                    if 'attachments' in mail.keys():
                        attachments_list = util.get_out_file_list(mail.get('attachments', []))
                        list_size = len(attachments_list)
                        if list_size == 0:
                            mail = error_mail("邮件结果过大，请降低图片大小")
                            server.send_mail(sent_from[0]['email'], mail)
                        mail_subject = mail['subject']
                        for i in range(list_size):
                            mail['subject'] = mail_subject + f'({i+1}/{list_size})'
                            mail['attachments'] = attachments_list[i]
                            server.send_mail(sent_from[0]['email'], mail)
                            print(f'({i+1}/{list_size}) send Success：{attachments_list[i]}')
                            print(mail)
                    else:
                        server.send_mail(sent_from[0]['email'], mail)
                        print(mail)

                    imbox.mark_seen(uid)
                    print('send Success\n')
            except Exception as e:
                print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + f"Error : {e}\n")
                if 'Message too large' in str(e):
                    mail = error_mail("邮件结果过大，请降低图片大小，或将png图片格式改为jpg格式")
                elif 'Mailbox unavailable or access denied' in str(e):
                    print(f'『Mailbox unavailable or access denied』 in error info, will skip, message: {mail}\n')
                    imbox.mark_seen(uid)
                    continue
                # elif 'Connection unexpectedly closed' in str(e):
                #     print(f'『Connection unexpectedly closed』 in error info, will skip, message: {mail}\n')
                #     imbox.mark_seen(uid)
                #     continue
                else:
                    mail = error_mail(e)
                server.send_mail(sent_from[0]['email'], mail)
                print(f'send Success, message: {mail}\n')
                imbox.mark_seen(uid)
                continue
            # break;

            # 删除旧邮件
            # inbox_messages_before=imbox.messages(date__lt=delete_days_ago)
            # print(f"inbox_messages_before={inbox_messages_before}")
            # for uid, messages in inbox_messages_before:
            #     try:
            #         title = messages.subject
            #         sent_from = messages.sent_from
            #         receivedate = time.strftime("%Y%m%d %H:%M:%S", time.strptime(messages.date[0:24], '%a, %d %b %Y %H:%M:%S'))
            #         if int(receivedate[:8]) > int(datetime.datetime.strftime(delete_days_ago, r'%Y%m%d')):
            #             break
            #         print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S'), "删除邮件：",uid, f'在 {receivedate} 收到',sent_from,'的邮件，主题为：',title)
            #         imbox.delete(uid)
            #     except Exception as e:
            #         print(datetime.datetime.strftime(datetime.datetime.now(),r'%Y.%m.%d %H:%M:%S : ') + f"Error : {e}\n")
            #         print(f"删除邮件：{uid=}, {messages.sent_from=}")
            #         imbox.delete(uid)

if __name__ == "__main__":
    emailProcess()
