import cv2
import xlwt
import numpy as np
import os
import sys
sys.path.append("../")
import util
import tqdm
from PIL import Image, ImageDraw, ImageFont

import numpy as np
import vtk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh

def getProjectionDrawing(front_path, side_path, edge = 200) :
    print(f"front_path={front_path}, chars={side_path}, edge={edge}")

    # 获取文字图片
    # img = np.zeros((edge, edge), np.uint8)
    # img.fill(255)
    # text_color = (0, 0, 0)
    # front_img = util.cv2AddChineseText(img, '莫', (0, 0), text_color, edge)
    # util.imwrite(front_path, '', front_img)

    # img = np.zeros((edge, edge), np.uint8)
    # img.fill(255)
    # text_color = (0, 0, 0)
    # side_img = util.cv2AddChineseText(img, '少', (0, 0), text_color, edge)
    # util.imwrite(side_path, '', side_img)


    # 读取正面、侧面
    front_img = cv2.imread(front_path, 0)
    side_img = cv2.imread(side_path, 0)
    # 二值化
    _, front_img = cv2.threshold(front_img,127,255,cv2.THRESH_OTSU)
    _, side_img = cv2.threshold(side_img,127,255,cv2.THRESH_OTSU)

    # 裁边
    # front_img = util.crop_empty(front_img)
    # side_img = util.crop_empty(side_img)

    # front_img = util.resize_img(front_img, edge)
    # side_img = util.resize_img(side_img, edge)

    # # 二值化
    # _, front_img = cv2.threshold(front_img,127,255,cv2.THRESH_OTSU)
    # _, side_img = cv2.threshold(side_img,127,255,cv2.THRESH_OTSU)

    # 统一高度
    side_img = util.resize_img(side_img, front_img.shape[0])
    print(f"preprocess ok, {front_img.shape=}, {side_img.shape=}")
    util.imwrite(front_path, '_pre', front_img)
    util.imwrite(side_path, '_pre', side_img)
    print(f"{front_img.shape=}, {side_img.shape=}")

    # 建立三维数组，层、行、列
    array_3d = np.zeros((front_img.shape[0], front_img.shape[1], side_img.shape[1]), dtype=int)
    print(f"{array_3d.shape=}")

    # 遍历正面，设置三维数组
    for h in range(front_img.shape[0]):
        for w in range(front_img.shape[1]):
            if front_img[h, w] == 0:
                array_3d[h, w, :] = 1
    print(f"front_img set ok")

    # 遍历侧面，设置三维数组
    for h in range(side_img.shape[0]):
        for w in range(side_img.shape[1]):
            if side_img[h, w] != 0:
                # 无像素点，图片设置为0
                array_3d[h, :, w] = 0
    print(f"side_img set ok")
    
    # 遍历3D模型每一层，删除多余点
    point_num = 0
    delete_num = 0
    for z in range(array_3d.shape[0]):
        # print(array_3d[z])
        # print(front_img[z])
        # print(side_img[z])
        for y in range(array_3d.shape[1]):
            for x in range(array_3d.shape[2]): 
                if array_3d[z, y, x] == 1:
                    if front_img[z, y] != 0 and side_img[z, x] != 0:
                        array_3d[z, y, x] = 0
                        delete_num += 1
                        continue
                    if front_img[z, y] == 0:
                        front_img[z, y] = 255
                    if side_img[z, x] == 0:
                        side_img[z, x] = 255
                    point_num += 1
        # for y in range(array_3d.shape[1]):
        #     for x in range(array_3d.shape[2]): 
        #         print(array_3d[z, y, x], end=' ')
        #     print()
        # print(array_3d[z])
        # print(f'{array_3d.shape[0]=},{z=}--------------------------------------------------------')
    util.imwrite(front_path, '_post', front_img)
    util.imwrite(side_path, '_post', side_img)
    print(f"delete excess point ok, {delete_num=}, {point_num=}")


    # # 创建VTK PolyData对象
    # cube_poly_data = vtk.vtkAppendPolyData()
    # # 遍历数组
    # for z in range(array_3d.shape[0]):
    #     print(f"{array_3d.shape[0]=}, {z=}")
    #     for y in range(array_3d.shape[1]):
    #         for x in range(array_3d.shape[2]):
    #             if array_3d[z, y, x] == 1:
    #                 # 创建小立方体
    #                 cube = vtk.vtkCubeSource()
    #                 cube.SetXLength(1)
    #                 cube.SetYLength(1)
    #                 cube.SetZLength(1)
    #                 cube.SetCenter(x+0.5, y+0.5, z+0.5)  # 将立方体中心设置到格点位置
    #                 cube.Update()
    #                 # 将小立方体添加到PolyData对象中
    #                 cube_poly_data.AddInputData(cube.GetOutput())
    # print(f"create cube ok")
    
    # # 合并所有小立方体
    # cube_poly_data.Update()
    # print(f"merge all cube ok")

    # # 创建STL写入器
    # stl_writer = vtk.vtkSTLWriter()
    # stl_writer.SetFileName('cubes.stl')
    # stl_writer.SetInputData(cube_poly_data.GetOutput())
    # stl_writer.Write()


    # 显示3D模型图
    # 创建一个新的3D图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 设置x, y, z轴的值
    x, y, z = np.where(array_3d == 1)
    # 绘制所有的点(x, y, z)
    ax.scatter(x, y, z, zdir='z', c='red', s=20)
    # 设置轴标签和标题
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Representation of 0-1 Array')
    # 显示图形
    plt.show()
     
    # return msgOk([len(chars_ret), len(chars_ret[0])])
   
if __name__ == "__main__":
    getProjectionDrawing("./front.jpg", "./side.jpg", 100)
    # getProjectionDrawing("./front.jpg", "./side.jpg", 30)




# import numpy as np
# from skimage import measure
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection
# # import seaborn as sns

# # 创建一个0-1的3D numpy数组
# # 这只是一个例子，你可以替换为你自己的数组
# array_3d = np.random.randint(0, 2, (10, 10, 10))

# # 找到数组中所有为1的位置
# coords = np.where(array_3d == 1)

# # 创建一个3D图形
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_aspect('equal')

# # 创建一个空的Poly3DCollection对象
# p = Poly3DCollection()

# # 为每一个体素（值为1的位置）创建一个立方体，并添加到Poly3DCollection对象中
# for i, j, k in zip(coords[0], coords[1], coords[2]):
#     vert = [(i, j, k), (i+1, j, k), (i+1, j+1, k), (i, j+1, k),  # 底面
#             (i, j, k+1), (i+1, j, k+1), (i+1, j+1, k+1), (i, j+1, k+1)]  # 顶面
#     p.append(vert)

# # 设置颜色和其他属性
# p.set_edgecolor('k')
# p.set_facecolor('b')
# p.set_alpha(0.5)

# # 将Poly3DCollection对象添加到图形中
# ax.add_collection3d(p)

# # 设置坐标轴的限制和属性
# ax.set_xlim([0, array_3d.shape[0]])
# ax.set_ylim([0, array_3d.shape[1]])
# ax.set_zlim([0, array_3d.shape[2]])
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Representation of 0-1 Array')

# # 保存图像为png文件（你也可以选择其他格式，如jpg、pdf等）
# plt.savefig('3d_representation.png')

# # 显示图形（如果需要）
# plt.show()