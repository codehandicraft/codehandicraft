import cv2
import os

# blockSize代表的是线的粗细，对于小图或者内容紧凑的图，blockSize小一点效果更好。太小会导致线连不上。
# C参数代表的是啥我不是很清楚，不过该值越大，对噪声的过滤效果越好。太大会导致丢失很多线条。
def edge(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    img_edge = cv2.adaptiveThreshold(img, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=5,
                                     C=11)

    save_filename = '%s.jpg' % (os.path.basename(filename).split('.')[0])
    cv2.imwrite('./kfk_out.jpg', img_edge)

from BetterOpenSCAD import *

d = CUBE(10, 10, 10)

# for x in range(5):
#     for y in range(5):
        # d -= DRILL(4 + x * 8, 4 + y * 8, 2.4)
d -= CUBE(1, 1, 1, 0,0,0)
d -= CUBE(1, 1, 1, 9,0,0)

RENDER(d, "hello.stl")



if __name__ == "__main__":
    filename = './kfk.png'
    edge(filename)


# import numpy as np
# import vtk

# # 创建示例三维01数组
# array = np.array([
#     [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
#     [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
#     [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# ])

# # 创建VTK PolyData对象
# cube_poly_data = vtk.vtkAppendPolyData()
# # 遍历数组
# for z in range(array.shape[0]):
#     for y in range(array.shape[1]):
#         for x in range(array.shape[2]):
#             if array[z, y, x] == 1:
#                 # 创建小立方体
#                 cube = vtk.vtkCubeSource()
#                 cube.SetXLength(1)
#                 cube.SetYLength(1)
#                 cube.SetZLength(1)
#                 cube.SetCenter(x+0.5, y+0.5, z+0.5)  # 将立方体中心设置到格点位置
#                 cube.Update()
#                 # 将小立方体添加到PolyData对象中
#                 cube_poly_data.AddInputData(cube.GetOutput())
# # 合并所有小立方体
# cube_poly_data.Update()
# # 创建STL写入器
# stl_writer = vtk.vtkSTLWriter()
# stl_writer.SetFileName('cubes.stl')
# stl_writer.SetInputData(cube_poly_data.GetOutput())
# stl_writer.Write()