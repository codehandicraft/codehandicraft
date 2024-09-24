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

import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

# 加载图片
def load_image(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# 转换图片颜色空间
def get_image(image_path):
    image = load_image(image_path)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    return image

# 获取主要颜色
def get_colors(image, number_of_colors, show_chart):
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
    return rgb_colors

# RGB颜色转换为十六进制颜色
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# 创建颜色条形图
def create_color_bar(colors):
    bar = np.zeros((100,500,3), dtype = "uint8")
    startX = 0
    for color in colors:
        endX = startX + (500 // len(colors))
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 100), \
                      color.astype("uint8").tolist(), -1)
        startX = endX
    return bar

# 主函数
def main(image_path):
    image = get_image(image_path)
    colors = get_colors(image, 10, True)
    bar = create_color_bar(colors)
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

# 执行主函数
if __name__ == "__main__":
    main('yinlang.png')