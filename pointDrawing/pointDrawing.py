'''
点画
将原图像缩小之后，使用PIL中的convert('1')函数转换，即可实现
'''
from PIL import Image
import numpy as np
import cv2

# 获得矩形的宽或高


def get_min_0_len(img, is_col):
    raw = 0
    col = 1
    if is_col == 1:
        raw = 1
        col = 0

    min_len = img.shape[0]
    for mm in range(img.shape[raw]):
        i = 0
        for nn in range(img.shape[col]):
            if img[mm, nn] == 0:
                i += 1
            else:
                if i != 0:
                    min_len = min(min_len, i)
                i = 0
    return min_len

# 将一个黑色矩形缩小为一个像素点，并淡化


def reset_point(img, ral_len, col_len, point_pixel=180):
    if point_pixel == 0:
        point_pixel = 1
    point_num = 0
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] != 0:
                continue
            for i in range(ral_len):
                for j in range(col_len):
                    if mm + j < img.shape[0] and nn + col_len < img.shape[1]:
                        img[mm + j, nn + i] = 255
            if mm + ral_len // 2 < img.shape[0] and nn + col_len // 2 < img.shape[1]:
                img[mm + ral_len // 2, nn + col_len // 2] = point_pixel
                point_num += 1
    return point_num


def week_img(img, point_pixel):
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] < point_pixel:
                img[mm, nn] = point_pixel
    return img

# 图像旋转（以任意点为中心旋转）


def image_rotate(src, rotate=0):
    h, w = src.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), rotate, 1)
    img = cv2.warpAffine(src, M, (w, h))

    return img


def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 锐化
    image = cv2.filter2D(image, -1, kernel=kernel)

    # # 使用拉普拉斯滤波进行锐化处理
    # laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # # 将锐化后的图像与原图像进行加权融合，增强锐化效果
    # image = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0, image)

    cv2.imwrite("_out.jpg", image)
    return image


def change_pixel(img, src_pixel, dst_pixel):
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] < src_pixel:
                img[mm, nn] = dst_pixel
    return img


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


def getPointDrawing(path, ratio=1, point_pixel=180, new_size=80):
    pil_img = Image.open(path)
    pil_img = pil_img.rotate(-45, expand=1, fillcolor=(255, 255, 255, 255))
    pil_img.save(path[:-4] + "_1.jpg")
    gray_img = cv2.imread(path[:-4] + "_1.jpg", 0)
    gray_img = crop_empty(gray_img)
    cv2.imwrite(path[:-4] + "_1.jpg", gray_img)
    m, n = pil_img.size
    print(m, n)
    # new_size = 100
    resize_pil_img = pil_img.resize((new_size, new_size * n // m))
    print(m/new_size)
    point_img = resize_pil_img.convert('1')
    point_img = point_img.resize((ratio * m, ratio * n))

    # PIL图像转cv2图像
    cv_img = cv2.cvtColor(np.asarray(
        point_img.convert("L")), cv2.COLOR_BGR2BGRA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = crop_empty(cv_img)
    cv2.imwrite(path[:-4] + "_temp.jpg", cv_img)

    # point_img.save(path[:-4] + "_1.jpg")

    # resize_img2 = point_img.resize((ratio * m, ratio * n))

    # resize_img2.save(path[:-4] + "_temp.jpg")

    col_len = m//new_size
    ral_len = m//new_size
    print(ral_len, col_len)

    # point_num = reset_point(cv_img, ral_len, col_len, point_pixel)
    # print(f"point_num = {point_num}")

    # 将图像中的每个黑色矩形缩小为一个像素点，并淡化
    # ral_len = get_min_0_len(cv_img, 0)
    # col_len = get_min_0_len(cv_img, 1)

    gray_img = cv2.imread(path[:-4] + "_temp.jpg", 0)
    kernel = np.ones((m//new_size//3*2+1, m//new_size//3*2+1), np.uint8)
    gray_img = cv2.dilate(gray_img, kernel)
    week_pixel = 210
    gray_img = week_img(gray_img, week_pixel)
    # gray_img = image_rotate(gray_img,-45)
    gray_img = change_pixel(gray_img, week_pixel-1, 255)
    cv2.imwrite(path[:-4] + "_temp2.jpg", gray_img)
    print(f"save temp jpg OK!")

    print(gray_img.shape)

    # cv2.imwrite(path[:-4] + "_out.jpg", cv_img)
    return


if __name__ == "__main__":
    getPointDrawing("./out2_out.jpg", 1, 180, 400)
