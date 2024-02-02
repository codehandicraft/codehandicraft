import cv2
import xlwt
import numpy as np
import os
import sys
import tqdm
import math
from PIL import Image, ImageDraw, ImageFont
sys.path.append("../")
import util

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    image = cv2.filter2D(image, -1, kernel=kernel)
    return image

# 输出图像的宽度 = 空白部分的(ratio+1)倍
def getCircleDrawing(path, circle_num = 12, thickness = 2, week_pixel=220):
    # 打印输入参数

    print(f"{path=}, {circle_num=}, {thickness=}, {week_pixel=}")
    # 处理输入图片，翻转图片
    img = cv2.imread(path, 0)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    _, img = cv2.threshold(img,60,255,cv2.THRESH_OTSU)
    img = custom_blur_demo(img)
    cv2.imwrite(path[:-4] + "_tmp.jpg", img)
    print(f"img size = {img.shape}")
    img = util.resize_img(img, 5000)

    # m, n = img.shape
    certer_point = (img.shape[1] // 2, img.shape[0] // 2)
    max_radius = max(img.shape[0], img.shape[1]) // 2
    interval = max(max_radius // circle_num, 1)
    print(f"{certer_point=}, {max_radius=}, {interval=}")

    # 生成同心圆圈
    circle_img = np.zeros(img.shape, np.uint8)
    circle_img.fill(255)
    for i in range(circle_num):
        cv2.circle(circle_img, certer_point, i * interval, 0, thickness)
    cv2.imwrite(path[:-4] + "_circle.jpg", circle_img)
    print("同心圆生成成功")

    # 根据圆圈覆盖范围，为图像赋值
    dst_img = np.zeros(img.shape, np.uint8)
    dst_img.fill(255)
    for m in range(img.shape[0]):
        for n in range(img.shape[1]):
            if circle_img[m, n] == 0:
                dst_img[m, n] = img[m, n]
    print("圆心画生成成功")
    # 保存输出图片
    cv2.circle(dst_img, certer_point, thickness, 0, -1)   
    cv2.imwrite(path[:-4] + "_out.jpg", dst_img)

    # # 顺时针旋转
    # dst_img = util.rotate_img(dst_img, 45)
    # _, dst_img = cv2.threshold(dst_img,160,255,cv2.THRESH_OTSU)
    # out_path = util.imwrite(path, '_rotate', dst_img)
    # print(f"顺时针旋转成功")

    dst_img = util.under_pixel_to_dst(dst_img, week_pixel, week_pixel)
    # 标记圆心
    cv2.circle(dst_img, certer_point, thickness, 0, -1)   
    cv2.imwrite(path[:-4] + "_week.jpg", dst_img)
    print(f"图像淡化成功, {week_pixel=}")

    return msgOk([len(dst_img), len(dst_img[0])])
    # return msgOk("")

if __name__ == "__main__":
    getCircleDrawing("./zlys4.jpg", 105, 2, 240)

