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

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    image = cv2.filter2D(image, -1, kernel=kernel)
    return image

# 输出图像的宽度 = 空白部分的(ratio+1)倍

def getCircleDrawing(path_list, para_list):
    # -------------- 解析参数 -----------------#
    para_list = util.merge_param(para_list, [100, 2, 240])
    print(f"input param list={para_list}")
    path = path_list[0]
    circle_num = para_list[0]
    thickness = para_list[1]
    week_pixel = para_list[2]

    out_path_list = []

# def getCircleDrawing(path, circle_num = 12, thickness = 2, week_pixel=220):
    # 打印输入参数
    print(f"{path=}, {circle_num=}, {thickness=}, {week_pixel=}")
    # 处理输入图片，翻转图片
    img = cv2.imread(path, 0)
    if (img is None):
        print("找不到待处理图片")
        return util.msgErr("找不到待处理图片")
    _, img = cv2.threshold(img,60,255,cv2.THRESH_OTSU)
    img = custom_blur_demo(img)
    print(f"img size = {img.shape}")
    img = util.resize_img(img, 5000)
    cv2.imwrite(path[:-4] + "_tmp.jpg", img)

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
    cv2.imwrite(path[:-4] + f"_out_{circle_num}.jpg", dst_img)

    # 顺时针旋转
    rotate_img = util.rotate_img(dst_img, 45)
    _, rotate_img = cv2.threshold(rotate_img,160,255,cv2.THRESH_OTSU)
    out_path = util.imwrite(path, f'_rotate_{circle_num}', rotate_img)
    out_path_list.append(out_path)
    print(f"顺时针旋转成功")

    # dst_img = util.under_pixel_to_dst(dst_img, week_pixel, week_pixel)
    dst_img = util.get_week_img(dst_img, week_pixel)
    # 标记圆心
    cv2.circle(dst_img, certer_point, thickness, 0, -1)   
    cv2.imwrite(path[:-4] + f"_week_{circle_num}.jpg", dst_img)
    print(f"图像淡化成功, {week_pixel=}")

    # 顺时针旋转
    dst_img = util.rotate_img(dst_img, 45)
    out_path = util.imwrite(path, f'_week_rotate_{circle_num}', dst_img)
    print(f"顺时针旋转成功")

    tip_info = """"""
    return util.msgOk({
        "out_path_list":out_path_list, 
        "in_param_list":para_list, 
        "tip_info":tip_info,
    })

if __name__ == "__main__":
    getCircleDrawing(["./bto.jpg"], [100, 2, 240])
    
    # img = cv2.imread('huahuoa_out_week.jpg', 0)  
    # print(img.shape) 
    # img = cv2.copyMakeBorder(img, 100, 100, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    # print(img.shape)
    # cv2.imwrite("huahuoa_out_week2.jpg", img)


