"""
双面点光源投影画
"""
import cv2
import numpy as np
import os
import math
import sys
sys.path.append("../")
from rasterBar import rasterBar
import util
from PIL import Image, ImageDraw, ImageFont
import matplotlib.path as mpath
from tqdm import tqdm

from sympy import *

def compute_plane_equation(P, Q, R):
    """
    计算过点P、Q、R的平面方程系数。
    返回平面方程的系数A, B, C, D。
    """
    # 将元组转换为numpy数组
    P = np.array(P)
    Q = np.array(Q)
    R = np.array(R)
    
    # 计算两个向量PQ和PR
    PQ = Q - P
    PR = R - P
    
    # 计算法向量N = PQ x PR
    N = np.cross(PQ, PR)
    N = N / np.linalg.norm(N)  # 归一化法向量
    
    # 计算平面方程中的d（即-D），并返回系数
    d = -np.dot(N, P)
    return N.tolist(), d

def compute_intersection(P, Q, R, E, N):
    """
    计算直线E、N与过点P、Q、R的平面的交点。
    P, Q, R, E, N均为元组坐标。
    返回交点的坐标（如果存在且为元组格式）。
    """
    # 将元组坐标转换为numpy数组
    P, Q, R, E, N = map(np.array, (P, Q, R, E, N))
    
    # 获取平面方程系数
    A, B, C, D = compute_plane_equation(P, Q, R)[0] + [compute_plane_equation(P, Q, R)[1]]
    
    # 直线E、N的方向向量
    dir_vector = N - E
    
    # 判断直线是否与平面平行
    if np.isclose(A*dir_vector[0] + B*dir_vector[1] + C*dir_vector[2], 0):
        return None  # 直线与平面平行或重合，无唯一交点
    
    # 计算参数t并获取交点坐标
    t = -(A*E[0] + B*E[1] + C*E[2] + D) / (A*dir_vector[0] + B*dir_vector[1] + C*dir_vector[2])
    intersection = E + t * dir_vector
    
    # 将交点坐标转换为元组格式并返回
    return tuple(intersection)

def point_in_quadrilateral(A, B, C, D, X):
    # 四边形四个点的坐标
    quad_coords = [A, B, C, D]

    # 创建一个四边形路径
    quad_path = mpath.Path(quad_coords + [quad_coords[0]])

    # 判断点X是否在四边形内
    return quad_path.contains_point(X)

def get_intersection_3d_xy_plane(M, P, x):
    # 提取M和P的x和y坐标，z坐标在xy平面上为0，因此可以忽略
    x1, y1 = M[:2]
    x2, y2 = P[:2]
    
    # 检查直线MP是否与直线x=c平行（即垂直于y轴）
    if x1 == x2:
        # 如果直线MP垂直于y轴且c与此直线x坐标相同，则整条直线都是交点
        if x == x1:
            # 返回任意一个y坐标对应的点，这里选择y1
            return (x, y1, 0)  # 在xy平面上，z坐标为0
        else:
            # 直线MP与直线x=c没有交点
            return None
    
    # 使用两点式确定直线MP在xy平面上的方程，并求解与直线x=c的交点
    slope = (y2 - y1) / (x2 - x1)
    y = y1 + slope * (x - x1)
    return (x, y, 0)  # 在xy平面上，z坐标为0

def distance_3d(P, Q):
    x1, y1, z1 = P
    x2, y2, z2 = Q
    # 计算两点间的距离
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance

def horizontal_distance_3d(P, Q):
    x1, y1, _ = P  # 使用 _ 忽略 z1 坐标
    x2, y2, _ = Q  # 使用 _ 忽略 z2 坐标
    # 计算水平距离
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def get_point_light_projection_drawings(path, img, white_image, point_light_N, point_light_M, P_x, Q_x, para_list, out_path_list):
    base_size_cm = para_list[0] # 投影画面尺寸-厘米
    point_light_height_cm = para_list[1] # 点光源高度-厘米
    projection_num = para_list[2] # 分割线数目
    path_name = os.path.splitext(path)[0]
    print(f"# ---------------------- 确定分割线&投影画面尺寸 start ------------------------- #")
    # 确定分割线 和 对应的投影画面尺寸
    point_P_list = []
    point_Q_list = []
    projection_img_list = []
    img_height, img_width = white_image.shape[:2]
    img_tmp = img.copy()
    for i in range(projection_num):
        # 动点P 
        point_P = (P_x, img_height * i // (projection_num - 1), 0)
        point_P_list.append(point_P)

        # 与另一个点光源在y轴上的交点
        point_Q = get_intersection_3d_xy_plane(point_P, point_light_M, x=Q_x)
        point_Q_list.append(point_Q)

        # 辅助线
        # print(f"{point_P=}, {point_Q=}, {img.shape=}")
        cv2.line(img_tmp, (int(point_P[0]), int(point_P[1])), (int(point_Q[0]), int(point_Q[1])), (0, 0, 255), thickness=2)
        # img = cv2.putText(img, f"{path_name}_{i}.jpg", (int(point_P[0]), int(point_P[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.line(white_image, (int(point_P[0]), int(point_P[1])), (int(point_Q[0]), int(point_Q[1])), (0, 0, 255), thickness=2)
        white_image = cv2.putText(white_image, f"{path_name}_{i}.jpg", (int(point_P[0]), int(point_P[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

        # 动点P 与 y轴交点Q 的距离，作为图片的宽度。高度为点光源高度
        point_P_Q_distance = math.ceil(horizontal_distance_3d(point_P, point_Q))
        # projection_img = Image.new('RGB', (point_P_Q_distance, point_light_N[2]), (255, 255, 255))
        projection_img = util.get_empty_img((int(point_light_N[2])+1, point_P_Q_distance+2), False)
        projection_img_list.append(projection_img)
        print(f"{point_P=}, {point_Q=}, {point_P_Q_distance=}, {projection_img.shape=}")
    # 防止溢出，额外加一组PQ点
    point_P_list.append((P_x, img_height + 1, 0))
    point_Q_list.append((Q_x, img_height, 0))
    util.imwrite(path, f'_crop', img_tmp)
    print(f"动点P、Q确定完毕，投影空白图片生成完成。")
    
    print(f"# ---------------------- START 填充投影画面 ---------------------- #")
    # 遍历原始平面图片像素点，与光源N相交于投影画面，并将像素点填充到投影画面中
    for y in tqdm(range(img_height)):
        # print(f"{img_height=}, {y=}")
        for x in range(img_width):
            # 计算像素点与光源N的交点
            img_point = (x, y, 0)
            for i in range(projection_num):
                if point_in_quadrilateral(point_P_list[i][:2], point_Q_list[i][:2], point_Q_list[i+1][:2], point_P_list[i+1][:2], img_point[:2]):
                    # 计算 PQ竖直平面 与 像素点-光源N 的交点F
                    intersection_point_F = compute_intersection(point_P_list[i], point_Q_list[i], (point_Q_list[i][0], point_Q_list[i][1], point_light_N[2]), img_point, point_light_N)
                    if intersection_point_F is None:
                        # 跳过没有交点的情况，不应该出现
                        print(f"{img_point=}, {point_light_N=}, {point_P_list[i]=}, {point_Q_list[i]=}, {intersection_point_F=}")
                        continue
                    # if int(intersection_point_F[2]) == 0:
                    #     # 忽略水平面上的交点
                    #     continue

                    # 交点距离y轴处的P、Q点的水平距离
                    if Q_x == 0:
                        distance_width = horizontal_distance_3d(point_Q_list[i], intersection_point_F)
                    else:
                        distance_width = horizontal_distance_3d(point_P_list[i], intersection_point_F)

                    # 投影画面像素值 设置为对应的水平像素点
                    try:
                        intersection_point_F_h = int(projection_img_list[i].shape[0] - intersection_point_F[2])
                        if intersection_point_F_h >= projection_img_list[i].shape[0]:
                            continue
                        projection_img_list[i][intersection_point_F_h, int(distance_width)] = img[y, x]
                    except Exception as e:
                        print(f"{(x,y)=}, {i=}, {(intersection_point_F_h, int(distance_width))}, {projection_img_list[i].shape=}, {intersection_point_F}, {e}")
                    img[y, x] = (0,0,0)
                    break
    print(f"投影图片生成完成。")
    util.imwrite(path, f'_moved_pixel', img)
    util.imwrite(path, f'_white_image', white_image)

    print(f"# ---------------------- START 保存图片 ---------------------- #")
    for i in range(len(projection_img_list)):
        projection_img = util.crop_top_empty(projection_img_list[i])
        print_width_cm = base_size_cm / img_height * projection_img.shape[1]
        projection_img = cv2.putText(projection_img, f"{print_width_cm:.2f}cm {path_name}_{i}.jpg", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        out_path_list.append(util.imwrite(path, f'_out_crop_{i}', projection_img))
        print(f"打印宽度：{print_width_cm:.2f}cm，裁剪后_out_crop_{i}：{projection_img.shape}")
    print(f"投影图片裁剪完成。")

    return projection_img_list


def getPointLightProjectionDrawing(path_list, para_list):
    print(f"# ---------------------- START 解析参数 ---------------------- #")
    para_list = util.merge_param(para_list, [30, 5, 5, 1])
    print(f"input param list={para_list}")
    base_size_cm = para_list[0] # 投影画面尺寸-厘米
    point_light_height_cm = para_list[1] # 点光源高度-厘米
    projection_num = para_list[2] # 分割线数目

    print(f"# ---------------------- START 解析图片 ---------------------- #")
    img_list = util.get_img_list(path_list)

    out_path_list = []
    path1 = path_list[0]
    path2 = path_list[1]
    
    print(f"# ---------------------- START 图片预处理 ---------------------- #")
    # 图片预处理，填充空白统一尺寸
    util.unify_size(img_list)
    img1 = img_list[0]
    img2 = img_list[1]
    # TODO 追加白边
    # cv2.copyMakeBorder(img, img.shape[0]//(projection_num+1), 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    # 统一为正方形图片
    img1 = util.unify_h_w_ratio_by_fill_blank(img1, 1, 1)
    img2 = util.unify_h_w_ratio_by_fill_blank(img2, 1, 1)

    util.imwrite(path1, f'_unify', img1)
    util.imwrite(path2, f'_unify', img2)
    print(f"图片预处理 完毕。{img1.shape=}, {img2.shape=}")

    print(f"# ---------------------- START 确定各个点 ---------------------- #")
    # 图片宽高
    img_height, img_width = img1.shape[:2] 
    print(f"确定宽高：{img_height=}, {img_width=}")

    # 辅助图片
    white_image = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255
    white_image = cv2.circle(white_image, (white_image.shape[0]//2, white_image.shape[1]//2), 3, 0, -1)  
    print(f"辅助图片新建完成：{white_image.shape=}")


    print(f"\n# ====================================== START 处理图片一 ====================================== #")
    white_image = cv2.putText(white_image, "N1", (white_image.shape[0]//2, white_image.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
    # 光源点N
    point_light_Y = img_height // 2
    point_light_Z = point_light_height_cm * img_height / base_size_cm
    point_light_N = (img_width // 2, -point_light_Y, point_light_Z)
    # 光源点M
    point_light_M = (-point_light_Y, point_light_Y, point_light_Z)
    print(f"光源点确定完毕。{point_light_N=}, {point_light_M=}, {white_image.shape=}")
    # 获取投影画面
    projection_img_list = get_point_light_projection_drawings(path1, img1, white_image, point_light_N, point_light_M, img_width, 0, para_list, out_path_list)    


    print(f"\n# ====================================== START 处理图片二 ====================================== #")
    # 底图顺时针旋转，N点不变，M点相对x=N[0]轴对称，P点在y轴上，Q点在右侧边AB上
    # 底图顺时针旋转
    white_image = util.rotate_img(white_image, 90)
    white_image = cv2.putText(white_image, "N2", (white_image.shape[0]//2, white_image.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
    util.imwrite(path1, f'_white_image_rotate', white_image)
    # 光源点M
    point_light_M = (2 * point_light_N[0] - point_light_M[0] , point_light_M[1], point_light_M[2])
    print(f"光源点确定完毕。{point_light_N=}, {point_light_M=}, {white_image.shape=}")
    # 获取投影画面
    projection_img_list = get_point_light_projection_drawings(path2, img2, white_image, point_light_N, point_light_M, 0, img_width, para_list, out_path_list)


#     # ---------------------- 返回结果 -------------------------#
#     tip_info = f"""预计共有2张图片附件，一张为拼接好的图片、一张为光栅条(用于测试效果预览)
# 使用的光栅片规格为{lpi}lpi,
# 请将拼接好的图片原比例以高度为{H_cm}cm的尺寸打印（参考宽度大约为{W_cm}cm）,

# tips:
# 1、建议图片的个数在2-4之间，图片个数过多效果并不好。有几张图片成品就有几变
# 2、每个参数用一个空格隔开，或者每个参数各占一行
# 3、每一行参数都需要为整数，暂不支持小数

# 各个参数的意思:
# 0、目前支持的参数共有4个，列如：50 5 600 0
# 1、第一个参数：光栅片的lpi值，整数
# 2、第二个参数：想要打印的成品图片高度，单位为cm
# 3、第三个参数：打印机的dpi值（不知道的可以写600或1200）
# 4、第四个参数：是否为竖条纹，0为横条纹(上下变)，1为竖条纹(左右变)

# 名词解释：
# dpi：每英寸点数（Dots Per Inch），指的是图像中每英寸长度内的像素点数量，是输出设备如打印机分辨率的量度单位之一
# lpi：指每英寸单位所包括的光栅条数（Lines Per Inch）

# 关键公式：
# 图片分割像素 = dpi / (图片个数 * lpi)
# 图片输出像素 = dpi * 图片打印尺寸(厘米) / 2.54

#             """
#     print(f"{tip_info=}")
#     return util.msgOk({
#             "out_path_list":out_path_list, 
#             "in_param_list":para_list, 
#             "tip_info":tip_info,
#         })

   
if __name__ == "__main__":

    # projection_img = cv2.imread("0_out_crop_0.jpg")
    # projection_img = cv2.putText(projection_img, f"31.67cm", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # util.imwrite("0_out_crop_0_test.jpg", f'', projection_img)

    getPointLightProjectionDrawing(["./0.jpg", "./111.jpg"], [30, 10, 5, 1])
    

