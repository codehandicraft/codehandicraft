'''
点画
将原图像缩小之后，使用PIL中的convert('1')函数转换，即可实现
'''
from PIL import Image
import numpy as np
import cv2
import sys
sys.path.append("../")
import util

# 获得矩形的宽或高
def get_min_0_len(img, is_col):
    """
    找到图片中全为0的连续序列的最大长度
    
    Args:
        img: numpy数组类型，表示待处理的图片
        is_col: int类型，表示图片的列数，如果is_col为1，则表示列数，如果is_col为0，则表示行数
    
    Returns:
        int类型，表示图片中全为0的连续序列的最大长度
    """
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

def getPointDrawing(path_list, para_list):
    # 解析参数
    para_list = util.merge_param(para_list, [350, 205, 1])
    print(f"input param list={para_list}")
    new_size = para_list[0]
    week_pixel = para_list[1]
    ratio = para_list[2]
    if len(path_list) < 1:
        return util.msgErr("path_list is empty")
    path = path_list[0]
    out_path_list = []

    # 统一高度
    gray_img = cv2.imread(path, 0)
    print(f"图片原始尺寸={gray_img.shape}")
    gray_img = crop_empty(gray_img)
    # gray_img = util.resize_img(gray_img, 1500)
    # gray_img = cv2.resize(gray_img, None, fx=0.5, fy=0.5)
    util.imwrite(path, '', gray_img)

    # 图片旋转
    pil_img = Image.open(path)
    pil_img = pil_img.rotate(-45, expand=1, fillcolor=255)
    # pil_img = pil_img.rotate(-90, expand=1, fillcolor=255)
    pil_img.save(path[:-4] + "_1.jpg")
    gray_img = cv2.imread(path[:-4] + "_1.jpg", 0)
    gray_img = crop_empty(gray_img)
    cv2.imwrite(path[:-4] + "_1.jpg", gray_img)
    m, n = pil_img.size
    print(f"旋转后图片尺寸={pil_img.size}")

    # 点阵化
    # new_size = 100
    resize_pil_img = pil_img.resize((new_size, new_size * n // m))
    print(f"缩放比例={m/new_size}")
    point_img = resize_pil_img.convert('1')
    point_img = point_img.resize((ratio * m, ratio * n))    # ratio为图片放大比例

    # PIL图像转cv2图像
    cv_img = cv2.cvtColor(np.asarray(
        point_img.convert("L")), cv2.COLOR_BGR2BGRA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = crop_empty(cv_img)
    out_path_list.append(util.imwrite(path, f"_{new_size}_out", cv_img))
    print("out img is ok")

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
    
    gray_img = cv2.imread(path[:-4] + f"_{new_size}_out.jpg", 0)
    # only week
    gray_img2 = gray_img.copy()
    _img = week_img(gray_img2, week_pixel)
    util.imwrite(path, f"_only_week_{week_pixel}", _img)
    _img = week_img(gray_img2, week_pixel+2)
    util.imwrite(path, f"_only_week_{week_pixel+2}", _img)
    _img = week_img(gray_img2, week_pixel+4)
    util.imwrite(path, f"_only_week_{week_pixel+4}", _img)

    # 溶解
    kernel = np.ones((m//new_size//3*2+1, m//new_size//3*2+1), np.uint8)
    gray_img = cv2.dilate(gray_img, kernel)
    util.imwrite(path, "_dilate", gray_img)

    # 淡化
    gray_img = week_img(gray_img, week_pixel)
    out_path_list.append(util.imwrite(path, f"_week_{week_pixel}", gray_img))
    print(f"save week img jpg OK!")

    print(f"{out_path_list=}")

    return util.msgOk({"out_path_list":out_path_list, "in_param_list":para_list})


if __name__ == "__main__":
    # A3打印：only_week 240灰度，week 230灰度
    # A4打印：only_week 250灰度，week 245灰度
    path_list = ["./feixiao1.jpg"]
    # para_list = [530, 249]      # point
    # para_list = [500, 251]      # point
    para_list = [500, 243]      # point
    # para_list = [320, 215]    # line
    getPointDrawing(path_list, para_list)
