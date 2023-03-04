import cv2
import xlwt
import numpy as np
import os
import sys
import tqdm
from PIL import Image, ImageDraw, ImageFont

diceImg = [0,]

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

# 中文字体乱码修复
def cv2AddChineseText(img, text, position=(0, 0), textColor=(255, 255, 255), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("./charDrawing/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def normalize(val, min_val, max_val, max=255, min=0):
    return (val - min_val) * (max - min) / (max_val - min_val) + min

def char_normalize(char_avg_img, max=255, min=0):
    char_avg_img = sorted(char_avg_img, key=lambda x:x[1], reverse=False) # 升序
    min_val = char_avg_img[0][1]
    max_val = char_avg_img[len(char_avg_img) - 1][1]
    char_avg_img = [[char, normalize(avg, min_val, max_val), img] for char, avg, img in char_avg_img]
    return char_avg_img

def get_char_img(char_avg_img, pixel):
    # 按序判断，找到就返回
    for i in range(len(char_avg_img) - 1):
        if pixel < (char_avg_img[i][1] + char_avg_img[i + 1][1]) / 2:
            return char_avg_img[i]
    return char_avg_img[len(char_avg_img) - 1]

def getCharDrawing(path, chars, edge = 200) :
    print(f"path={path}, chars={chars}, edge={edge}")
    # 字符_平均像素_字符图像
    char_avg_img = []
    for char in chars:
        img = np.zeros((30, 30), np.uint8)
        char_imgs = cv2AddChineseText(img, char, (0, 0), (255, 255, 255), 30)
        # cv2.imwrite(path[:-4] + f"_{char}.jpg", char_imgs)
        
        print(f"char={char}, avg={int(np.mean(char_imgs))}")
        char_avg_img.append([char, np.mean(char_imgs), char_imgs])
    # 允许存在空字符
    char_avg_img.append(["　", 1, cv2.cvtColor(np.zeros((30, 30), np.uint8), cv2.COLOR_RGB2BGR)])

    # 对字符的平均像素进行排序、归一化处理
    char_avg_img = char_normalize(char_avg_img)
    
    # 处理输入图片，灰度并归一化
    img = cv2.imread(path, 0)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)

    # 图片规格处理
    img_height, img_width = img.shape
    ratio = edge / (img_width if img_height > img_width else img_height)
    img = cv2.resize(img, None, fx=ratio, fy=ratio)

    # 根据图像计算所有骰子点数
    height, width = img.shape
    char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    chars_ret = [[0 for _ in range(width)] for _ in range(height)]
    print(f"图像的文字规格为{len(chars_ret)}*{len(chars_ret[0])}")
    for i in range(len(chars_ret)):
        for j in range(len(chars_ret[i])):
            chars_ret[i][j], _, char_imgs_ret[i][j] = get_char_img(char_avg_img, img[i, j])

    # 保存文字结果
    with open(path[:-4] + "_out.txt", 'w+') as file:    
        lines = [''.join(line) + "\n" for line in chars_ret]
        file.writelines(lines) 

    # 保存输出图片
    # imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_imgs_ret])
    # cv2.imwrite(path[:-4] + "_out.jpg", imgOut)

    return msgOk([len(chars_ret), len(chars_ret[0])])
   
if __name__ == "__main__":
    getCharDrawing("./charDrawing/linghua-r.png", "我是神里绫华的狗", 300)

