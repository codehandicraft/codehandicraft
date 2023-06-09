import cv2
import xlwt
import numpy as np
import os
import sys
import tqdm
import math
from PIL import Image, ImageDraw, ImageFont

diceImg = [0,]

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

# 输出图像的宽度 = 空白部分的(ratio+1)倍
def getReflexDrawing(path, angle = 270, ratio = 3):
    # 处理输入图片，翻转图片
    img = cv2.imread(path)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    img = cv2.flip(img, 0)
    # img = cv2.resize(img, None, fx=0.1, fy=0.1)
    
    # 拼接空白图片，用于放置圆柱镜面
    empty_img = np.zeros((img.shape[0] // ratio, img.shape[1], 3), np.uint8)
    empty_img.fill(255)
    img = np.concatenate([empty_img, img], axis=0)
    # cv2.imwrite(path[:-4] + "_temp.jpg", img)

    # 创建目标图片，大小为2m*2m
    # m * n, m行n列
    m, n, _= img.shape
    newimg = np.zeros((2 * m, 2 * m, 3), np.uint8)
    newimg.fill(255)
    # 根据对应关系，赋予原图形的像素值
    for y in range(newimg.shape[0]):
        for x in range(newimg.shape[1]):
            x2 = int(n * math.atan2(m - y, x - m) / math.pi * 180 / angle)
            if m - y < 0:
                x2 = int(n * (math.atan2(m - y, x - m) / math.pi * 180 + 360) / angle)
            y2 = int(math.sqrt((x - m) ** 2 + (y - m) ** 2))
            if x2 >= n or y2 >= m:
                newimg[y, x, :] = 255
            else:
                newimg[y, x, :] = img[y2, x2, :]
    # 标记圆心
    cv2.circle(newimg, (m, m), 3, (0, 0, 0), -1)   

    # 保存输出图片
    cv2.imwrite(path[:-4] + "_out.jpg", newimg)
    return msgOk([len(newimg), len(newimg[0])])
    # return msgOk("")
   
if __name__ == "__main__":
    getReflexDrawing("./out2.jpg", 270)

