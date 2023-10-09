import cv2
import os
import numpy as np
import math

# height, width = img.shape[:2] 

def under_pixel_to_dst(img, src_pixel, dst_pixel):
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] < src_pixel:
                img[mm, nn] = dst_pixel
    return img

def upwards_pixel_to_dst(img, src_pixel, dst_pixel):
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] > src_pixel:
                img[mm, nn] = dst_pixel
    return img

def get_square_img(img):
    img = cv2.resize(img, (img.shape[0], img.shape[0]))
    return img

# 获得指定shape的空白图片
def get_empty_img(shape):
    empty_img = np.zeros(shape, np.uint8)
    empty_img.fill(255)
    return empty_img

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

def imwrite(path, suffix, img):
    path_pair = os.path.splitext(path)
    cv2.imwrite(path_pair[0] + suffix + ".jpg", img)
    return path_pair[0] + suffix + ".jpg"
    # cv2.imwrite(path_pair[0] + suffix + path_pair[1], img)
    # return path_pair[0] + suffix + path_pair[1]

# 裁边，裁剪掉>=src_pixel的部分
def crop_empty(img, src_pixel=255):
    # 灰度图
    gray_img = img
    if img.ndim != 2:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for i in range(4):
        for mm in range(gray_img.shape[0]):
            for nn in range(gray_img.shape[1]):
                if gray_img[mm, nn] < src_pixel:
                    if mm > 0:
                        img = img[mm:img.shape[0], :]
                        gray_img = gray_img[mm:gray_img.shape[0], :]
                    break
            else:
                continue
            break
        # 顺时针90度
        img = cv2.flip(cv2.transpose(img), 1)
        gray_img = cv2.flip(cv2.transpose(gray_img), 1)

    return img

import cv2  
  
def crop_white_border(img):  
    # 转换为灰度图像  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
      
    # 二值化处理  
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  
      
    # 寻找轮廓  
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
      
    # 找到最大的轮廓  
    max_contour = max(contours, key=cv2.contourArea)  
      
    # 计算最大轮廓的边界框  
    rect = cv2.boundingRect(max_contour)  
      
    # 绘制边界框  
    # cv2.rectangle(img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)  
      
    # 裁剪图像  
    crop_img = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]  
      
    return crop_img

# 通过填充空白，统一尺寸
def unify_size(imgs):
    print("unify size start")
    max_h = 0
    max_w = 0
    for img in imgs:
        h, w= img.shape[:2]
        if h > max_h:
            max_h = h
        if w > max_w:
            max_w = w
    print(f"max_h={max_h}, max_w={max_w}")
    
    for i in range(len(imgs)):
        h, w = imgs[i].shape[:2]
        top = math.ceil((max_h - h) / 2)
        bottom = math.floor((max_h - h) / 2)
        left = math.ceil((max_w - w) / 2)
        right = math.floor((max_w - w) / 2)
        print(f"ori_shape={imgs[i].shape}, h={h}, w={w}, top={top}, bottom={bottom}")

        imgs[i] = cv2.copyMakeBorder(imgs[i], top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        print(imgs[i].shape)

    return imgs

# 填充空白图片，达到指定长宽比
def unify_h_w_ratio_by_fill_blank(img, h, w):
    # 约分
    h,w = get_gcd(h, w)
    print(f"fill_blank: img_shape={img.shape[:2]}, h={h}, w={w}")
    # 最大比例
    ratio = max(img.shape[0] // h, img.shape[1] // w)
    if h * ratio - img.shape[0] < 0 or w * ratio - img.shape[1] < 0:
        ratio += 1
    # 统一长宽比
    new_h = h * ratio
    new_w = w * ratio
    print(f"{ratio=}, {new_h=}, {new_w=}")
    # 填充空白
    top = math.ceil((new_h - img.shape[0]) / 2)
    bottom = math.floor((new_h - img.shape[0]) / 2)
    left = math.ceil((new_w - img.shape[1]) / 2)
    right = math.floor((new_w - img.shape[1]) / 2)
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    return img

# 裁剪图片，达到指定长宽比
def unify_h_w_ratio_by_crop_img(img1, h, w):
    print(f"crop_img: img_shape={img1.shape[:2]}, h={h}, w={w}")
    h,w = get_gcd(h, w)
    print(f"crop_img: img_shape={img1.shape[:2]}, gcd_h={h}, gcd_w={w}")
    img1_new_h = min(img1.shape[0] // h, img1.shape[1] // w) * h
    img1_new_w = min(img1.shape[0] // h, img1.shape[1] // w) * w
    img1 = img1[(img1.shape[0]-img1_new_h)//2: img1.shape[0]-(img1.shape[0]-img1_new_h) //
                2, (img1.shape[1]-img1_new_w)//2: img1.shape[1]-(img1.shape[1]-img1_new_w)//2]
    return img1

def resize_img(img, dst_h):
    h, w = img.shape[:2]
    return cv2.resize(img, (w * dst_h // h, dst_h))

def get_gcd(h, w):
    h = int(h * 100)
    w = int(w * 100)
    gcd = math.gcd(h, w)
    h //= gcd
    w //= gcd
    return h, w

def create_dir(path):
    try:
        os.makedirs(path)
        print(f"{path}目录创建成功！")
    except FileExistsError:
        print(f"{path}目录已存在！")

def merge_param(input_param, default_param):
    if len(input_param) >= len(default_param):
        return input_param
    for i in range(len(input_param)):
        default_param[i] = input_param[i]
    return default_param