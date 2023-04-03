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

def normalize(val, min_val, max_val, max=255, min=0):
    return (val - min_val) * (max - min) / (max_val - min_val) + min

def save_hist(path, img):
    empty_img = np.zeros((256, 256), np.uint8)
    empty_img.fill(255)
    img_b = cv2.calcHist(img,[0],None,[256],[0,255])
    for mm in range(img_b.shape[0]):
        for y in range(int(img_b[mm, 0])):
            empty_img[y, mm] = 0
    empty_img = cv2.flip(empty_img, 0)
    cv2.imwrite(path[:-4] + "_hist.jpg", empty_img)

# 输出所有像素值,去重
def print_pixel(img):
    cal_list=[]
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] not in cal_list:
                cal_list.append(img[mm, nn])
    cal_list.sort()
    print(cal_list)

# 裁边，四周灰度>=src_pixel的部分都会被裁剪
def crop_empty(img, src_pixel=255):
    for i in range(4):
        for mm in range(img.shape[0]):
            for nn in range(img.shape[1]):
                if img[mm, nn] < src_pixel:
                    if mm > 0:
                        img = img[mm:img.shape[0], :]
                    break
            else:
                continue
            break  
        # 顺时针90度
        img = cv2.flip(cv2.transpose(img), 1)
    
    return img


def getShadowDrawing(path, gradient=5) :
    
    # 处理输入图片，灰度并归一化
    gray_img = cv2.imread(path, 0)
    if (gray_img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    
    # 裁边
    gray_img = crop_empty(gray_img)
    cv2.imwrite(path[:-4] + "_gray.jpg", gray_img)

    # Canny算子
    Canny = cv2.Canny(gray_img, 50, 150)
    cv2.imwrite(path[:-4] + "_canny.jpg", 255-Canny)

    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(gray_img)
    print(minVal, maxVal)
    # 灰度条，共gradient+1个灰度
    color_img_list=[]
    for i in range(gradient + 1):
        empty_img = np.zeros((gray_img.shape[0]//gradient, gray_img.shape[1]//10), np.uint8)
        empty_img.fill((maxVal - minVal) // gradient * i + minVal)
        print((maxVal - minVal) // gradient * i + minVal)
        color_img_list.append(empty_img)
    color_img = np.concatenate(color_img_list, axis=0)
    cv2.imwrite(path[:-4] + "_color.jpg",color_img)
    color_img = cv2.resize(color_img, (gray_img.shape[1]//10, gray_img.shape[0]))
    
    # 灰度值量化，映射到gradient+1个灰度中
    gray_img = (gray_img - minVal) // ((maxVal - minVal) / gradient) * ((maxVal - minVal) / gradient) + minVal
    cv2.imwrite(path[:-4] + "_out.jpg", gray_img)

    # # 溶解
    # kernel = np.ones((3,3), np.uint8)
    # gray_dilation =cv2.erode(gray_img, kernel)
    # gray_erosion =cv2.dilate(gray_dilation, kernel)
    # # gray_erosion = np.concatenate([gray_erosion, color_img], axis=1)
    # cv2.imwrite(path[:-4] + "_dilation.jpg", gray_erosion)
    
    # # 淡化
    # _dilation = cv2.imread(path[:-4] + "_dilation.jpg", 0)
    # Canny = 255-cv2.Canny(_dilation, 50, 150)
    # for mm in range(Canny.shape[0]):
    #     for nn in range(Canny.shape[1]):
    #         if Canny[mm, nn] == 0:
    #             Canny[mm, nn]=200
    # cv2.imwrite(path[:-4] + "_canny-res.jpg", (Canny))
    

    return msgOk([len(gray_img), len(gray_img[0])])
   
if __name__ == "__main__":
    getShadowDrawing("./naxida_test.jpg", 5)

