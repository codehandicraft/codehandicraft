import cv2
import xlwt
import numpy as np
import os
import sys
sys.path.append("../")
import util
import tqdm
from PIL import Image, ImageDraw, ImageFont


def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

def getCollageDrawing(src_path, resource_path, edge = 100, color = [0, 0, 0]) :
    # 参数检查
    print(f"path={src_path}, resource_path={resource_path}, edge={edge}")

    # 零件图
    resource_img = cv2.imread(resource_path, 0)
    resource_img = util.resize_img(resource_img, 30)
    _, part_threshold_img = cv2.threshold(resource_img, 127, 255, cv2.THRESH_BINARY)
    red_img = np.zeros((part_threshold_img.shape[0], part_threshold_img.shape[0], 3), dtype=np.uint8)  
    red_img[:, :] = [255, 255, 255]
    for i in range(len(part_threshold_img)):
        for j in range(len(part_threshold_img[i])):
            if part_threshold_img[i][j] == 255:
                red_img[i][j] = [255, 255, 255]
            else:
                red_img[i][j] = [0, 0, 255]
    part_threshold_img = red_img
    util.imwrite(resource_path, "_thre", part_threshold_img)

    # 空白零件图
    empty_part_img = util.get_empty_img((30,30), False)
    certer_point = (empty_part_img.shape[1] // 2, empty_part_img.shape[0] // 2)
    cv2.circle(empty_part_img, certer_point, 2, (203, 192, 255), -1)   
    util.imwrite(resource_path, "_part", empty_part_img)

    # 原始图缩小、二值化
    gray_img = cv2.imread(src_path, 0)
    gray_img = util.resize_img(gray_img, edge)
    util.imwrite(src_path, f"_resize_{edge}", gray_img)
    _, gray_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    util.imwrite(src_path, "_thre", gray_img)

    # 替换为0的像素点
    height, width = gray_img.shape
    empty_img = util.get_empty_img(part_threshold_img.shape)
    char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    empty_part_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    chars_ret = [[0 for _ in range(width)] for _ in range(height)]
    part_num = 0
    for i in range(len(chars_ret)):
        for j in range(len(chars_ret[i])):
            chars_ret[i][j] = gray_img[i, j]
            if gray_img[i, j] == 0:
                char_imgs_ret[i][j] = part_threshold_img
                empty_part_imgs_ret[i][j] = empty_part_img
                part_num += 1
            else:
                char_imgs_ret[i][j] = empty_img
                empty_part_imgs_ret[i][j] = empty_img
    print(f"图像的规格为{len(chars_ret)}*{len(chars_ret[0])}, {part_num=}")
    
    # 保存输出图片
    imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_imgs_ret])
    print(imgOut.shape)
    util.imwrite(src_path, "_out", imgOut)

    # 保存打印图片
    print_img = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in empty_part_imgs_ret])
    print(print_img.shape)
    util.imwrite(src_path, "_out_print", print_img)


    # 返回结果
    return msgOk([len(chars_ret), len(chars_ret[0])])
   
if __name__ == "__main__":
    getCollageDrawing("./yz2.jpg", "./resource/flower.jpg", 100)
