import cv2
import numpy as np

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