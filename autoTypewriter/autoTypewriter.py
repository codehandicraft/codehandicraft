'''
双面画，输入两张图片，横向交叉合并成一张，
参考：https://www.zadmei.com/rhzpzmnj.html
'''
import sys
sys.path.append("../")
import pohan
from pohan.pinyin.pinyin import Style
import time
import keyboard
import pyautogui
import os
import util
import cv2

def autoTypewriter(input_file_list, param_int_list):
    sleep_time = 1
    print(f"start to sleep {sleep_time}s")
    time.sleep(sleep_time)
    print(f"start to typewrite")

    with open(input_file_list[0], 'r') as f:
        line = f.readline()
        i=1
        while line:
            # 文字转拼音
            pinyin_line = ''
            for char in line:
                # print(f"文字： {char}")
                if char == '　':
                    char = ' '
                pinyin = pohan.pinyin.han2pinyin(char, errors='default', style=Style.NORMAL)[0][0]
                # print(f"拼音： {pinyin}")
                # ********* 特别设置，使用首字母即可 *********
                if pinyin != 'da' and pinyin != 'si' and pinyin != 'li':
                    pinyin = pinyin[0]
                if pinyin != '\n' and pinyin != ' ':
                    pinyin += ' '
                pinyin_line += pinyin
            
            # 去除右侧所有空格
            pinyin_line = pinyin_line.rstrip("\n")
            pinyin_line = pinyin_line.rstrip(" ")
            pinyin_line += " \n"
            # print(f"pinyin_line = [{pinyin_line}]")

            # 模拟键盘输入
            pyautogui.typewrite(pinyin_line)
            print(f"第{i}行已完成...")
            # if i == 10:
            # break
            i += 1
            line = f.readline()
    return


if __name__ == "__main__":
    input_path_list = ['./tp.txt']
    # input_path_list = ['./demo.txt']
    autoTypewriter(input_path_list, [])
