"""
光栅画
"""
import cv2
import numpy as np
import os
import sys
sys.path.append("../")
from rasterBar import rasterBar
import util
from PIL import Image, ImageDraw, ImageFont

def getRasterCard(path_list, para_list):
    # -------------- 解析参数 -----------------#
    para_list = util.merge_param(para_list, [50, 5, 600, 1])
    print(f"input param list={para_list}")
    lpi = para_list[0]
    # 厘米转英寸
    H_cm = para_list[1]
    dpi = para_list[2]
    # 竖条纹-左右变
    is_h = para_list[3]==1

    # -------------- 解析图片 -----------------#
    if len(path_list) < 2 or len(path_list) > 10:
        print(f'input_file_list is empty, will return failed_mail')
        return util.msgErr('输入图片数量小于2或大于10', '请上传2~10张图片；\n图片不要用超大附件发送；\n图片放在附件中')
    img_list = []
    out_path_list = []
    for path in path_list:
        img = cv2.imread(path)
        if img is None:
            print(f"找不到待处理图片, path={path}")
            return util.msgErr("存在图片无法读取", "可以将图片发到qq重新保存再通过邮件发送过来")
        img_list.append(img)
        print(path, img.shape)
    # 统一 img list 尺寸， 固定长宽比
    util.unify_size_by_crop_img(img_list)
    W_cm = H_cm * img_list[0].shape[1] / img_list[0].shape[0]

    # -------------- 计算图片尺寸和分片尺寸 -----------------#
    # 图片个数
    img_num = len(img_list)
    # 每个分片的像素
    per_pixel = int(dpi / (img_num * lpi))
    # 图片的输出像素
    # H_pixel = int((H_cm/2.54) * (img_num * lpi * per_pixel))
    # W_pixel = int((W_cm/2.54) * (img_num * lpi * per_pixel))
    H_pixel = int((H_cm/2.54) * dpi)
    W_pixel = int((W_cm/2.54) * dpi)
    print(f"{img_num=}, {per_pixel=}, {H_cm=}, {W_cm=}, {is_h=}, {H_pixel=}, {W_pixel=}")
    
    for i in range(len(img_list)):
        # 竖条纹，统一宽度
        if is_h:
            img_list[i] = util.resize_img_w(img_list[i], W_pixel)
        # 横条纹，同一高度
        else:
            img_list[i] = util.resize_img(img_list[i], H_pixel)
    for i in range(len(img_list)):
        util.imwrite(path_list[i], f'_resize', img_list[i])

    # -------------- 图片合并 -----------------#
    raster_img = rasterBar.merge_img_list(img_list, per_pixel, is_h)
    W_cm = H_cm * raster_img.shape[1] / raster_img.shape[0]
    out_path_list.append(util.imwrite(path_list[0], f'_lpi{lpi}_{is_h}_out', raster_img))

    # 生成光栅条纹PNG图片
    raster_bar_path = util.gen_new_path(path_list[0], f'_lpi{lpi}_{is_h}_bar', '.png')
    rasterBar.gen_raster_png_img(raster_bar_path, per_pixel, int(raster_img.shape[0]), int(raster_img.shape[1]), len(img_list), is_h)
    out_path_list.append(raster_bar_path)
    print(f"光栅图生成成功")

    # -------------- 返回结果 -----------------#
    tip_info = f"""预计共有2张图片附件，一张为拼接好的图片、一张为光栅条(用于测试效果预览)
使用的光栅片规格为{lpi}lpi,
请将拼接好的图片原比例以高度为{H_cm}cm的尺寸打印（参考宽度大约为{W_cm}cm）,

tips:
1、建议图片的个数在2-4之间，图片个数过多效果并不好。有几张图片成品就有几变
2、每个参数用一个空格隔开，或者每个参数各占一行
3、每一行参数都需要为整数，暂不支持小数

各个参数的意思:
0、目前支持的参数共有4个，列如：50 5 600 0
1、第一个参数：光栅片的lpi值，整数
2、第二个参数：想要打印的成品图片高度，单位为cm
3、第三个参数：打印机的dpi值（不知道的可以写600或1200）
4、第四个参数：是否为竖条纹，0为横条纹(上下变)，1为竖条纹(左右变)

名词解释：
dpi：每英寸点数（Dots Per Inch），指的是图像中每英寸长度内的像素点数量，是输出设备如打印机分辨率的量度单位之一
lpi：指每英寸单位所包括的光栅条数（Lines Per Inch）

关键公式：
图片分割像素 = dpi / (图片个数 * lpi)
图片输出像素 = dpi * 图片打印尺寸(厘米) / 2.54

            """
    print(f"{tip_info=}")
    return util.msgOk({
            "out_path_list":out_path_list, 
            "in_param_list":para_list, 
            "tip_info":tip_info,
        })

   
if __name__ == "__main__":
    # getRasterCard(["./input/20240308161034_223_308128/0.jpg", 
    #                "./input/20240308161034_223_308128/1.jpg", 
    #                "./input/20240308161034_223_308128/2.jpg", 
    #                "./input/20240308161034_223_308128/3.jpg", 
    #                ], 
    #                [42, 5, 600, 1])
    # getRasterCard(["./hh1.png", "./hh2.jpg"], [50, 10, 1200, 1])
    getRasterCard(["./huahuo1.png", "./huahuo2.png"], [32, 5, 600, 0])

