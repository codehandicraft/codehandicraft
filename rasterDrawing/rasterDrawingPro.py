"""
光栅画
"""
import cv2
import xlwt
import numpy as np
import os
import sys
sys.path.append("../")
import util
import tqdm
from PIL import Image, ImageDraw, ImageFont

def unify_img_list_size(img_list):
    m1, n1 = img_list[0].shape
    for i in range(1, len(img_list)):
        img2 = img_list[i]
        m2, n2 = img2.shape
        # 统一高度
        img2 = cv2.resize(img2, (m1 * n2 // m2, m1))
        
        
        # img2 = util.crop_img(img2, m1, n1)


        img_list[i] = img2
    for img in img_list:
        print(img.shape)
    return img_list


def getRasterDrawingPro(path_list, para_list):
    # 解析参数
    para_list = util.merge_param(para_list, [50, 10, 600, 0])
    print(f"input param list={para_list}")
    # raster_num = para_list[0]
    # week_pixel = para_list[1]
    # ratio = para_list[2]
    lpi = para_list[0]
    h_in = para_list[1]/2.54
    dpi = para_list[2]
    # 竖条纹
    is_h = para_list[3]==1
    # ratio = para_list[2]

    if len(path_list) < 2 or len(path_list) > 10:
        return util.msgErr("img num is not valid")
    img_list = []
    out_path_list = []
    for path in path_list:
        img = cv2.imread(path)
        # img = util.under_pixel_to_dst(img, 235, 0)
        # _, img = cv2.threshold(img, 235, 255, cv2.THRESH_BINARY)
        img_list.append(img)
        print(path, img.shape)

    # 计算高度
    img_num = len(img_list)
    per_pixel = int(dpi / (img_num * lpi))
    # per_pixel = 4
    h_pixel = int(h_in * (img_num * lpi * per_pixel))
    print(f"{img_num=}, {per_pixel=}, {h_pixel=}")
    
    for i in range(len(img_list)):
        # 统一宽度
        if is_h:
            img_list[i] = util.resize_img_w(img_list[i], h_pixel)
        # 同一高度
        else:
            img_list[i] = util.resize_img(img_list[i], h_pixel)
        
    # 统一 img list 尺寸
    util.unify_size(img_list)
    for i in range(len(img_list)):
        util.imwrite(path_list[i], f'_resize', img_list[i])
    print(f"统一尺寸ok, {img_list[0].shape}")

    # util.unify_h(img_list)
    # util.unify_size(img_list)

    raster_img = img_list[0]
    img_height = raster_img.shape[0]
    img_width = raster_img.shape[1]
    pixel_num = per_pixel
    if is_h:
        #============= 合成光栅画-竖条纹 =============#
        # 遍历，目标图片分片 = 循环取出原图片的分片
        i = 0
        j = 0
        while (i + 1) * pixel_num <= img_width:
            raster_img[:, i * pixel_num : (i + 1) * pixel_num] = img_list[j][:, i * pixel_num : (i + 1) * pixel_num]
            j = (j + 1) % len(img_list)
            i += 1
        out_path_list.append(util.imwrite(path_list[0], f'_pro_out_{dpi}', raster_img))
        print(f"光栅画生成成功-竖条纹")
    else:
        # #============= 合成光栅画-横条纹 =============#
        # 遍历，目标图片分片 = 循环取出原图片的分片
        i = 0
        j = 0
        while (i + 1) * pixel_num <= img_height:
            raster_img[i * pixel_num : (i + 1) * pixel_num, :] = img_list[j][i * pixel_num : (i + 1) * pixel_num, :]
            j = (j + 1) % len(img_list)
            i += 1
        out_path_list.append(util.imwrite(path_list[0], f'_pro_out_{dpi}', raster_img))
        print(f"光栅画生成成功-竖条纹")



    # 生成光栅
    gen_raster_img(pixel_num, raster_img.shape[0], int(raster_img.shape[1]), len(img_list), is_h)
    print(f"光栅图生成成功")

    # return msgOk([len(chars_ret), len(chars_ret[0])])

def gen_raster_img(stripe_width, image_height, image_width, img_num, is_h):
    # 设置条纹的宽度和图像的总尺寸
    # stripe_width = 50  # 每条条纹的宽度
    # image_width = 4 * stripe_width  # 图像的总宽度（这里设置为4条条纹的宽度）
    # image_height = 100  # 图像的总高度

    # 创建一个空的RGBA图像（包含透明度通道）
    img = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    pixels = np.array(img)  # 将图像转换为NumPy数组以便更高效的操作

    # 设置黑色条纹和透明条纹
    black_color = (0, 0, 0, 255)  # 黑色（不透明）
    transparent_color = (0, 0, 0, 0)  # 透明色

    if is_h:
        # 填充条纹
        for x in range(0, image_height, img_num * stripe_width):
        # 黑色条纹
            pixels[x:x+stripe_width*(img_num-1), 0:image_width] = black_color
            
            # 检查是否还有空间绘制下一条透明条纹
            if x + stripe_width < image_height:
                # 透明条纹
                pixels[x+stripe_width*(img_num-1):x+img_num*stripe_width, 0:image_width] = transparent_color

    else:
        # 填充条纹
        for x in range(0, image_width, img_num * stripe_width):
            # 黑色条纹
            pixels[0:image_height, x:x+stripe_width*(img_num-1)] = black_color
            
            # 检查是否还有空间绘制下一条透明条纹
            if x + stripe_width < image_width:
                # 透明条纹
                pixels[0:image_height, x+stripe_width*(img_num-1):x+img_num*stripe_width] = transparent_color

    # 将NumPy数组转回PIL图像
    img = Image.fromarray(pixels)

    # 保存图像
    img.save('black_and_transparent_stripes.png')


   
if __name__ == "__main__":
    getRasterDrawingPro(["./huahuo1.png", "./huahuo2.png"], [75, 10, 300, 1])
    # getRasterDrawingPro(["./huahuo1.png", "./huahuo2.png"], [75, 10, 1200])

