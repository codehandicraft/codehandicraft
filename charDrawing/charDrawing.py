import cv2
import xlwt
import numpy as np
import os
import sys
sys.path.append("../")
import math
import util
import tqdm
from PIL import Image, ImageDraw, ImageFont

diceImg = [0,]

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

# 中文字体乱码修复
def cv2AddChineseText(img, text, position=(0, 0), textColor=(255, 255, 255), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    # fontStyle = ImageFont.truetype("./charDrawing/simsun.ttc", textSize, encoding="utf-8")
    fontStyle = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", textSize, encoding="utf-8")
    # fontStyle.set_variation_by_name("bold")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def normalize(val, min_val, max_val, max=255, min=0):
    return (val - min_val) * (max - min) / (max_val - min_val) + min

def char_normalize(char_avg_img, max=255, min=0):
    char_avg_img = sorted(char_avg_img, key=lambda x:x[1], reverse=False) # 升序
    min_val = char_avg_img[0][1]
    max_val = char_avg_img[len(char_avg_img) - 1][1]
    char_avg_img = [[char, normalize(avg, min_val, max_val), img] for char, avg, img in char_avg_img]
    return char_avg_img

def get_char_img(char_avg_img, pixel):
    # 按序判断，找到就返回
    for i in range(len(char_avg_img) - 1):
        if pixel < (char_avg_img[i][1] + char_avg_img[i + 1][1]) / 2:
            return char_avg_img[i]
    return char_avg_img[len(char_avg_img) - 1]

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    image = cv2.filter2D(image, -1, kernel=kernel)

    # # 使用拉普拉斯滤波进行锐化处理
    # laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # # 将锐化后的图像与原图像进行加权融合，增强锐化效果
    # image = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0, image)

    cv2.imwrite("_out.jpg", image)
    return image

def gen_html(path, img_color, chars_ret):
    html_head = '''<!DOCTYPE html>
<html>
<head> 
<meta charset="utf-8"> 
<title>字符画(由B站莫少Kilig提供技术支持)</title> 
</head> 
<body style="background-color:rgb(0,0,0);font-size:1px">'''
    with open(path[:-4] + "_out.html", 'w+') as file:   
        lines = [html_head,'\n']
        for i in range(len(chars_ret)):
            for j in range(len(chars_ret[i])): 
                line = f'<text style="color:rgb({img_color[i, j][2]},{img_color[i, j][1]},{img_color[i, j][0]})">{chars_ret[i][j]} </text>'
                lines.append(line)
            lines.append('<br>\n')
        lines.append('</body>\n</html>')
        file.writelines(lines) 
    print("gen html char result ok")
    return path[:-4] + "_out.html"

def unify_h_w_ratio_by_crop_img(img1, h, w):
    print(f"crop_img: before img_shape={img1.shape[:2]}, h={h}, w={w}")
    img1_new_h = min(img1.shape[0] // h, img1.shape[1] // w) * h
    img1_new_w = min(img1.shape[0] // h, img1.shape[1] // w) * w

    left = math.ceil((img1.shape[0]-img1_new_h) / 2)
    right = left + img1_new_h
    top = math.ceil((img1.shape[1]-img1_new_w)/2)
    bottom = top + img1_new_w

    # img1 = img1[(img1.shape[0]-img1_new_h)//2: img1.shape[0]-(img1.shape[0]-img1_new_h) //
    #             2, (img1.shape[1]-img1_new_w)//2: img1.shape[1]-(img1.shape[1]-img1_new_w)//2]
    img1 = img1[left:right, top:bottom]
    print(f"crop_img: after  img_shape={img1.shape[:2]}, h={h}, w={w}, {img1_new_h=}, {img1_new_w=}")
    return img1

def char_to_img(char, size=30):
    img = np.zeros((size, size), np.uint8)
    return cv2AddChineseText(img, char, (0, 0), (255, 255, 255), size)

def char_to_img_matrix(char, num, size=30):
    # 生成字符图片矩阵
    char_img_list = []
    for _ in range(num):
        char_img_list_line = []
        for _ in range(num):
            char_img_list_line.append(char_to_img(char, size))
        char_img_list.append(char_img_list_line)

    # 合并矩阵
    img_out = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_img_list])
    return cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)

def getCharDrawing(path, chars, edge = 200, is_color = True, is_white_back = False, char_BGR_color = []) :
    print(f"path={path}, chars={chars}, edge={edge}, is_color={is_color}")
    # 打印文字解释原理
    # line_list = ["\n"*19]
    # for i in [1,2,5,10,17,25]:
    #     line_list.append((" "*10 + "   ".join([char*i for char in chars]) + '\n') * i + "\n"*65)
    # with open(path[:-4] + "_demo.txt", 'w+') as file:    
    #     # lines = [''.join(line) + "\n" for line in line_list]
    #     file.writelines(line_list) 

    # 生成文字图片-用于解释原理
    demo_img_size = (1800,2880)
    demo_img_hight = demo_img_size[0]
    demo_img_width = demo_img_size[1]
    for i in [1,2,5,10,17,25]:
        demo_img = np.zeros(demo_img_size, np.uint8)
        demo_char_size = demo_img_width // (len(chars) + 1)
        interval_size = demo_char_size // (len(chars) - 1 + 6)
        chars_img = [char_to_img_matrix(char, i, demo_char_size//i) for char in chars]
        for idx, char_img in enumerate(chars_img):
            # util.imwrite(path, f"_demo_chars_img_{i}_{idx}.jpg", char_img)
            char_img_size = char_img.shape[0]
            # print(f"char_img.shape={char_img.shape}")
            
            start_x_pos = (demo_img_width - len(chars) * char_img_size - (len(chars)-1) * interval_size) // 2
            y1=demo_img_hight//2-char_img_size//2
            y2=y1+char_img_size
            x1=start_x_pos + idx*(interval_size+char_img_size)
            x2=x1+char_img_size
            demo_img[y1:y2, x1:x2] = char_img
        util.imwrite(path, f"_demo_{i}.jpg", demo_img)
    print(f"文字demo图片生成完成。")
    
    # 字符_平均像素_字符图像
    char_avg_img = []
    for char in chars:
        img = np.zeros((30, 30), np.uint8)
        text_color = (255, 255, 255)
        if is_white_back:
            img.fill(255)
            text_color = (0, 0, 0)
        char_imgs = cv2AddChineseText(img, char, (0, 0), text_color, 30)
        # cv2.imwrite(path[:-4] + f"_{char}.jpg", char_imgs)
        
        print(f"char={char}, avg={int(np.mean(char_imgs))}")
        char_avg_img.append([char, np.mean(char_imgs), char_imgs])
    # 允许存在空字符
    if is_white_back:
        char_avg_img.append(["　", 255, cv2.cvtColor(np.ones((30, 30), np.uint8), cv2.COLOR_RGB2BGR)])
    else:
        char_avg_img.append(["　", 1, cv2.cvtColor(np.zeros((30, 30), np.uint8), cv2.COLOR_RGB2BGR)])

    # 对字符的平均像素进行排序、归一化处理
    char_avg_img = char_normalize(char_avg_img)
    
    # 处理输入图片，灰度并归一化
    img = cv2.imread(path, 0)
    img_color = cv2.imread(path)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)

    # 保存为A3纸大小：297mm × 420mm，一个图片为3*3mm, 则文字list为 99个 * 140个
    if edge == 99:
        img = unify_h_w_ratio_by_crop_img(img, edge, 140)
    elif edge == 140:
        img = unify_h_w_ratio_by_crop_img(img, edge, 99)
    # 图片规格处理
    img_height, img_width = img.shape
    ratio = edge / (img_width if img_height > img_width else img_height)
    img = cv2.resize(img, None, fx=ratio, fy=ratio)
    img_color = cv2.resize(img_color, None, fx=ratio, fy=ratio)
    img = custom_blur_demo(img)
    cv2.imwrite(path[:-4] + "_out.jpg", img)
    cv2.imwrite(path[:-4] + "_out_color.jpg", img_color)

    # 指定坐标替换为指定文字
    hack_info = {
        # (117, 78): '我',
        # (117, 79): '是',
        # (117, 80): '流',
        # (117, 81): '萤',
        # (117, 82): '小',
        # (117, 83): '姐',
        # (117, 84): '的',
        # (117, 85): '狗',
    }
    # 根据图像计算所有骰子点数
    height, width = img.shape
    char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    color_char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    red_color_char_imgs_ret = [[0 for _ in range(width)] for _ in range(height)]
    chars_ret = [[0 for _ in range(width)] for _ in range(height)]
    chinese_char_num = 0  # 汉字字符数量
    print(f"图像的文字规格为{len(chars_ret)}*{len(chars_ret[0])}")
    for i in range(len(chars_ret)):
        for j in range(len(chars_ret[i])):
            chars_ret[i][j], _, char_imgs_ret[i][j] = get_char_img(char_avg_img, img[i, j])
            # 彩色字符画
            if is_color:
                color_char_img = np.zeros((30, 30, 3), np.uint8)
                color_BGR = img_color[i, j]
                if (i, j) in hack_info:
                    chars_ret[i][j] = hack_info[(i, j)]
                color_char_imgs_ret[i][j] = cv2AddChineseText(color_char_img, chars_ret[i][j], (0, 0), tuple([color_BGR[2], color_BGR[1], color_BGR[0]]), 30)
            if len(char_BGR_color):
                color_char_img = np.zeros((30, 30, 3), np.uint8)
                color_BGR = char_BGR_color
                red_color_char_imgs_ret[i][j] = cv2AddChineseText(color_char_img, chars_ret[i][j], (0, 0), tuple([color_BGR[2], color_BGR[1], color_BGR[0]]), 30)
                pass
            if chars_ret[i][j] != '　':
                chinese_char_num += 1
            # util.imwrite(path, f"_color_{chars_ret[i][j]}_{j}_{j}.jpg", color_char_imgs_ret[i][j])

    print(f"get char result ok, {chinese_char_num=}. start to write txt and img")
    # 生成html文件
    gen_html(path, img_color, chars_ret)
    # 生成xls文件
    util.save_list_to_xls(chars_ret, path[:-4] + "_out.xls")
    # 生成xlsx文件，，彩色Excel无法显示完全，因为内存不足，暂未解决
    # util.set_xls_color(chars_ret, img_color, path[:-4] + "_out.xlsx")
    # util.save_list_to_xlsx(chars_ret, img_color, path[:-4] + "_out.xlsx")
    # util.save_list_to_shard_xlsx(chars_ret, img_color, path[:-4] + "_out_shard.xlsx")
    # util.save_list_to_xlsxs(chars_ret, img_color, path[:-4] + "_out_s.xlsx")

    # 保存文字结果
    with open(path[:-4] + "_out.txt", 'w+') as file:    
        lines = [''.join(line) + "\n" for line in chars_ret]
        file.writelines(lines) 

    # 保存输出图片
    imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_imgs_ret])
    # imgOut = cv2.resize(imgOut, (img_height, width))
    out_path = util.imwrite(path, "_out", imgOut)
    if edge == 99 or edge == 140:
        out_path_img = cv2.imread(out_path, 0)
        img_week = util.upwards_pixel_to_dst(out_path_img, 100, 100)
        week_path = util.imwrite(path, "_week", img_week)
        print(f"{edge=}, get week result ok, {week_path=}")


    # 保存输出图片
    if is_color:
        imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in color_char_imgs_ret])
        # imgOut = cv2.resize(imgOut, (img_height, width))
        cv2.imwrite(path[:-4] + "_color_out.jpg", imgOut)
    if len(char_BGR_color):
        imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in red_color_char_imgs_ret])
        # imgOut = cv2.resize(imgOut, (img_height, width))
        cv2.imwrite(path[:-4] + "_red_color_out.jpg", imgOut)

    return msgOk([len(chars_ret), len(chars_ret[0])])

def char_file_to_img(path, char_size=30, is_white_back=False):
    # 打开字符文件
    with open(path, 'r') as file:
        lines = file.readlines()
        # 读取字符文件
        char_imgs_ret = []
        for line in lines:
            line_char_imgs = []
            for char in line:
                if char == "\n":
                    continue
                if char == "　":
                    line_char_imgs.append(cv2.cvtColor(np.ones((char_size, char_size), np.uint8), cv2.COLOR_RGB2BGR))
                else:
                    img = np.zeros((char_size, char_size), np.uint8)
                    text_color = (255, 255, 255)
                    if is_white_back:
                        img.fill(255)
                        text_color = (0, 0, 0)
                    line_char_imgs.append(cv2AddChineseText(img, char, (0, 0), text_color, char_size))
            char_imgs_ret.append(line_char_imgs)
        print(f"文字个数为{len(char_imgs_ret)}*{len(char_imgs_ret[0])}")
        print(f"图片尺寸为{char_size*len(char_imgs_ret)}*{char_size*len(char_imgs_ret[0])}")
        imgOut = cv2.vconcat([cv2.hconcat([char_img for char_img in ral_imgs]) for ral_imgs in char_imgs_ret])
        cv2.imwrite(path[:-4] + f"_file_to_img{char_size}_out.jpg", imgOut)
                                                          

if __name__ == "__main__":
    getCharDrawing("./charDrawing/hh2.jpg", "我是神里绫人的狗", 150, False, False, [])
    # getCharDrawing("./charDrawing/hh_char.jpg", "我是藿藿大人的狗", 100, False, False, [100, 100, 255])

