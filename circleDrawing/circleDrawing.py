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

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    image = cv2.filter2D(image, -1, kernel=kernel)
    return image

# 输出图像的宽度 = 空白部分的(ratio+1)倍
def getCircleDrawing(path, interval = 10, thickness = 2):
    # 处理输入图片，翻转图片
    img = cv2.imread(path, 0)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    # _, img = cv2.threshold(img,127,255,cv2.THRESH_OTSU)
    img = custom_blur_demo(img)
    cv2.imwrite(path[:-4] + "_tmp.jpg", img)

    # m, n = img.shape
    certer_point = (img.shape[0] // 2, img.shape[1] // 2)
    max_radius = min(img.shape[0], img.shape[1]) // 2

    # 生成同心圆圈
    circle_img = np.zeros(img.shape, np.uint8)
    circle_img.fill(255)
    for i in range(max_radius // interval):
        cv2.circle(circle_img, certer_point, i * interval, 0, thickness)

    # 根据圆圈覆盖范围，为图像赋值
    dst_img = np.zeros(img.shape, np.uint8)
    dst_img.fill(255)
    for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            if circle_img[m, n] == 0:
                dst_img[m, n] = img[m, n]

    # 标记圆心
    cv2.circle(dst_img, certer_point, thickness, 0, -1)   
    
    # 二值化
    _, dst_img = cv2.threshold(dst_img,127,255,cv2.THRESH_OTSU)

    # 保存输出图片
    cv2.imwrite(path[:-4] + "_out.jpg", dst_img)
    return msgOk([len(dst_img), len(dst_img[0])])
    # return msgOk("")
   
if __name__ == "__main__":
    getCircleDrawing("./linghua.png")

