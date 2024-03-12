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

def getRasterBar(path_list, para_list):
    # 解析参数
    para_list = util.merge_param(para_list, [100, 1, 1])
    print(f"input param list={para_list}")
    # 光栅个数
    raster_num = para_list[0]
    is_h = para_list[1]
    is_fill_blank_img = para_list[2]
    # week_pixel = para_list[3]
    if len(path_list) < 2 or len(path_list) > 10:
        return util.msgErr(f"获取到的图片数量为{len(path_list)}, 数量不正确")
    img_list = []
    out_path_list = []
    for path in path_list:
        img = cv2.imread(path)
        if img is None:
            print(f"找不到待处理图片, path={path}")
            return util.msgErr("找不到待处理图片")
        # 灰度图，二值化
        # img = cv2.imread(path, 0)
        # _, img = cv2.threshold(img, 235, 255, cv2.THRESH_BINARY)
        img_list.append(img)
        print(path, img.shape)
    print(f"图片读取ok, 图片个数len={len(img_list)}")

    if is_fill_blank_img:
        # 填充空白统一尺寸
        util.unify_h(img_list)
        util.unify_size(img_list)
    else:
        # 裁剪图片统一尺寸
        util.unify_size_by_crop_img(img_list)
    for i in range(len(img_list)):
        util.imwrite(path_list[i], f'_resize', img_list[i])
    print(f"统一尺寸ok, {img_list[0].shape}")

    # 多张图片合成一张光栅画
    pixel_num = img_list[0].shape[1] // raster_num
    if not is_h:
        pixel_num = img_list[0].shape[0] // raster_num
    raster_img = merge_img_list(img_list, pixel_num, is_h)
    out_path_list.append(util.imwrite(path_list[0], f'_{raster_num}_out', raster_img))

    # 图像淡化
    # week_pixel=252
    # util.week_img(path_list[0], raster_img, week_pixel)

    # 生成光栅条纹PNG图片
    raster_bar_path = util.gen_new_path(path_list[0], f'_bar', '.png')
    gen_raster_png_img(raster_bar_path, pixel_num, int(raster_img.shape[0]), int(raster_img.shape[1]), len(img_list), is_h)
    out_path_list.append(raster_bar_path)
    print(f"光栅图生成成功")

    return util.msgOk({
            "out_path_list":out_path_list, 
            "in_param_list":para_list, 
            "tip_info":f"""预计共有2张图片附件，一张为拼接好的图片，一张为光栅条
两张图片的打印尺寸必须相同，其中拼接的图片可以直接用普通纸打印，光栅条的处理方式有两种：
1、光栅条用普通纸打印，然后通过裁纸刀将白色部分裁掉
2、光栅条用透明菲林片打印，然后直接就可使用

tips:
1、建议图片的个数在2-4之间，图片个数过多效果并不好，因为遮挡的部分过多
2、每个参数用一个空格隔开，或者每个参数各占一行
3、每一行参数都需要为整数，暂不支持小数

解释下各个参数的意思:
    目前支持的参数共有3个，列如：100 1 1
    第一个参数为光栅条的个数。（100表示每张图片会被分割成100份）
    第二个参数（可选）为1时表示竖向条纹，为0时为纵向条纹
    第三个参数（可选）为1时表示填充空白统一图片尺寸，为0时为裁剪图片
            """,
        })


# 多张图片交叉合成一张
def merge_img_list(img_list, pixel_num, is_h):
    """
    将多张图片拼接成一张光栅画
    
    Args:
        img_list (list): 图片列表，每个元素为一张图片，格式为numpy数组
        pixel_num (int): 拼接每个小图的像素数
        is_h (bool): 是否为竖条纹光栅画，True为竖条纹，False为横条纹
    
    Returns:
        numpy.ndarray: 拼接后的光栅画，格式为numpy数组
    
    """
    raster_img = img_list[0]
    img_height = raster_img.shape[0]
    img_width = raster_img.shape[1]
    if is_h:
        #============= 合成光栅画-竖条纹 =============#
        # 遍历，目标图片分片 = 循环取出原图片的分片
        i = 0
        j = 0
        while (i + 1) * pixel_num <= img_width:
            raster_img[:, i * pixel_num : (i + 1) * pixel_num] = img_list[j][:, i * pixel_num : (i + 1) * pixel_num]
            j = (j + 1) % len(img_list)
            i += 1
        # out_path_list.append(util.imwrite(path_list[0], f'_pro_out_{dpi}', raster_img))
        print(f"光栅画生成成功-竖条纹")
    else:
        # #============= 合成光栅画-横条纹 =============#
        # 遍历，目标图片分片 = 循环取出原图片的分片
        i = 0
        j = 0
        while (i + 1) * pixel_num <= img_height:
            # print(f"{j=},{raster_img.shape=}, {img_list[j].shape=}, ")
            raster_img[i * pixel_num : (i + 1) * pixel_num, :] = img_list[j][i * pixel_num : (i + 1) * pixel_num, :]
            j = (j + 1) % len(img_list)
            i += 1
        # out_path_list.append(util.imwrite(path_list[0], f'_pro_out_{dpi}', raster_img))
        print(f"光栅画生成成功-横条纹")
    
    return raster_img

# 生成光栅条纹PNG图片
def gen_raster_png_img(out_path, stripe_width, image_height, image_width, img_num, is_h):
    """
    生成带有黑白条纹的PNG图片。
    
    Args:
        out_path (str): 输出的图片路径。
        stripe_width (int): 条纹宽度。
        image_height (int): 图片高度。
        image_width (int): 图片宽度。
        img_num (int): 图片数量。
        is_h (bool): 是否为水平条纹。
    
    Returns:
        None
    
    """
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

    if not is_h:
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
    img.save(out_path)

   
if __name__ == "__main__":
    getRasterBar(["./hh3.png", "./hh4.jpg"], [250])

