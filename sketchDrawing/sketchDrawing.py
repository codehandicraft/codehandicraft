# -*- coding: utf-8 -*-

'''
线稿画
参考 https://blog.csdn.net/xiangxueerfei/article/details/127750980?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-127750980-blog-122724653.pc_relevant_3mothn_strategy_recovery&spm=1001.2101.3001.4242.1&utm_relevant_index=3
'''
import sys
sys.path.append("../")
import util
import cv2
import numpy as np


def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 锐化
    image = cv2.filter2D(image, -1, kernel=kernel)

    # # 使用拉普拉斯滤波进行锐化处理
    # laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # # 将锐化后的图像与原图像进行加权融合，增强锐化效果
    # image = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0, image)

    cv2.imwrite("sis_out.jpg", image)
    return image


def getSketchDrawing(path_list, para_list=[127,0]):
    # 解析输入信息
    default_param = [200,0]
    para_list = util.merge_param(para_list, default_param)
    if para_list[0] <= 0 or para_list[0] >= 255:
        para_list = default_param
    path = path_list[0]
    threshold = para_list[0]
    is_B_W = para_list[1]
    print(f"path={path}, threshold={threshold}, is_B_W={is_B_W}")
    out_path_list = []

    # 读取图片
    image = cv2.imread(path)
    if (image is None):
        print("找不到待处理图片")
        return util.msgErr("找不到待处理图片")
    # 将BGR图像转换为灰度
    # image = util.crop_white_border(image)
    # util.imwrite(path, '_crop', image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ################### 黑白图像使用，将小于252像素的设置为0 ###################
    if is_B_W != 0:
        gray_image = util.under_pixel_to_dst(gray_image, threshold, 0)

    print("set gray_image ok")
    util.imwrite(path, '_gray', gray_image)

    # gray_image = cv2.resize(gray_image, None, fx=0.5, fy=0.5)
    util.imwrite(path, '_resize', gray_image)
    print(gray_image.shape)

    # 图像反转
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (15, 15), 0)
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    pencil_sketch = custom_blur_demo(pencil_sketch)
    util.imwrite(path, '_pencil_sketch', gray_image)

    dst = pencil_sketch
    rett, th1 = cv2.threshold(dst, threshold, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(
        dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 2)
    # 倒数第二个参数越小，线条越细
    th3 = cv2.adaptiveThreshold(
        dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 2)
    out_path_list.append(util.imwrite(path, '_orignal', dst))
    out_path_list.append(util.imwrite(path, '_threshold', th1))
    out_path_list.append(util.imwrite(path, '_adaptiveThreshold-MEAN', th2))
    out_path_list.append(util.imwrite(path, '_adaptiveThreshold-GAUSSIAN', th3))
    print("set threshold ok")

    # img = cv2.imdecode(np.fromfile("kfk_out.jpg",dtype=np.uint8),-1)
    fast = cv2.fastNlMeansDenoising(th1, None, 45, 7, 21)
    out_path_list.append(util.imwrite(path, '_fast-NlMeans', fast))
    fast2 = cv2.fastNlMeansDenoising(th2, None, 65, 7, 21)
    out_path_list.append(util.imwrite(path, '_fast-NlMeans2', fast2))
    # out_path_list.append(util.imwrite(path, '_medianBlur', cv2.medianBlur(th1, 3)))

    # out
    out_msg = {"out_path_list": out_path_list, "in_param_list":para_list}
    print(out_msg)
    return util.msgOk(out_msg)

if __name__ == "__main__":
    path_list = ["./huahuo4.jpg"]
    # path_list = ["./input/20231008213132_539_101423/0.png"]
    para_list = [235, 0]
    getSketchDrawing(path_list, para_list)
