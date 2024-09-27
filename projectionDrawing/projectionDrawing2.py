import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cv2

def img_to_surface(img):
    # 根据二值图像生成表面坐标
    surface = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] == 255:  # 假设物体部分的像素值为255
                surface.append((j, i))  # x, y坐标
    return surface

# 加载二值图像
top_view_img = plt.imread('front.jpg')
side_view_img = plt.imread('side.jpg')

# 转换为灰度并二值化
top_view = 255-cv2.cvtColor(top_view_img, cv2.COLOR_RGB2GRAY)
side_view = 255-cv2.cvtColor(side_view_img, cv2.COLOR_RGB2GRAY)
_, top_view = cv2.threshold(top_view, 127, 255, cv2.THRESH_BINARY)
_, side_view = cv2.threshold(side_view, 127, 255, cv2.THRESH_BINARY)

# 获取图像尺寸
tv_height, tv_width = top_view.shape
sv_height, sv_width = side_view.shape

# 创建三维空间（一个三维数组），初始值为0
volume = np.zeros((tv_height, tv_width, sv_height))

# 将主视图映射到顶面
for x, y in img_to_surface(top_view):
    volume[y, x, :] = 1

# 将侧视图映射到侧面，映射时需要旋转侧视图
for z, x in img_to_surface(side_view):
    volume[:, x, z] = volume[:, x, z] * 1  # 与顶面映射取交集

# 创建3D图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制3D模型的每个体素
for x in range(tv_width):
    for y in range(tv_height):
        for z in range(sv_height):
            if volume[y, x, z] == 1:
                # 绘制体素（这里简单地画一个点）
                ax.scatter(x, y, z, c='b', marker='s')

# 设置轴的比例相等
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, tv_width)
ax.set_ylim(0, tv_height)
ax.set_zlim(0, sv_height)
plt.gca().invert_yaxis()  # Y轴反向，以符合图像的坐标系统

# 显示结果
plt.show()