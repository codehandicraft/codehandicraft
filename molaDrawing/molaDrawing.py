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

def getMolaDrawing(path, chars, edge = 200) :
    print(f"path={path}, chars={chars}, edge={edge}")

    mola_path = './mola.jpg'
    mola_img = cv2.imread(mola_path, 0)
    shape = (30, 30)
    mola_img = cv2.resize(mola_img, shape)
    empty_img = util.get_empty_img(shape)
    # mola_img = util.get_square_img(mola_img)
    print(mola_img.shape)
    # mola_img = util.under_pixel_to_dst(mola_img, 127, 0)
    # mola_img = util.upwards_pixel_to_dst(mola_img, 127, 255)
    # mola_img = 255 - mola_img
    # cv2.imwrite(mola_path, mola_img)


    pil_img = Image.open(path)
    m, n = pil_img.size
    print(m,n)
    new_size = 100
    resize_pil_img = pil_img.resize((new_size, new_size * n // m))
    point_img = resize_pil_img.convert('1')
    # PIL图像转cv2图像
    cv_img = cv2.cvtColor(np.asarray(point_img.convert("L")), cv2.COLOR_BGR2BGRA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path[:-4] + "_point.jpg", cv_img)
    print(cv_img.shape)
    
    # return

    # # 图片规格处理
    # img_height, img_width = img.shape
    # ratio = edge / (img_width if img_height > img_width else img_height)
    # img = cv2.resize(img, None, fx=ratio, fy=ratio)
    # # img = custom_blur_demo(img)
    # cv2.imwrite(path[:-4] + "_out.jpg", img)

    # 根据图像计算所有骰子点数
    height, width = cv_img.shape
    char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    chars_ret = [[0 for _ in range(width)] for _ in range(height)]
    print(f"图像的文字规格为{len(chars_ret)}*{len(chars_ret[0])}")
    for i in range(len(chars_ret)):
        for j in range(len(chars_ret[i])):
            chars_ret[i][j] = cv_img[i, j]
            if cv_img[i, j] == 0:
                char_imgs_ret[i][j] = mola_img
            else:
                char_imgs_ret[i][j] = empty_img
    # # 保存文字结果
    # with open(path[:-4] + "_out.txt", 'w+') as file:    
    #     lines = [''.join(line) + "\n" for line in chars_ret]
    #     file.writelines(lines) 

    # 保存输出图片
    imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_imgs_ret])
    # imgOut = cv2.resize(imgOut, (img_height, width))
    print(imgOut.shape)
    cv2.imwrite(path[:-4] + "_out.jpg", imgOut)

    return msgOk([len(chars_ret), len(chars_ret[0])])
   
if __name__ == "__main__":
    getMolaDrawing("./out1.jpg", "我是妮露小姐的狗", 300)

