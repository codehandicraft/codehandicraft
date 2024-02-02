import cv2
import xlwt
import numpy as np
import os
import sys
import tqdm
import sys
sys.path.append("../")
import util

diceImg = [0,]

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

# 灰度量化，将灰度值转换到1-6
def getDiceNum(pixel):
    if (0 <= pixel and pixel <= 42):
        return 1
    elif (42 < pixel and pixel <= 84):
        return 2
    elif (84 < pixel and pixel <= 126) : 
        return 3
    elif (126 < pixel and pixel <= 168) : 
        return 4
    elif (168 < pixel and pixel <= 210) : 
        return 5
    elif (210 < pixel and pixel <= 255) : 
        return 6
    else :
        return 6

# 计算size*size范围内的像素平均值
def getAveragePixel(img, h_start, w_start, size) :
    sum = 0
    for i in range(h_start, h_start + size):
        for j in range(w_start, w_start + size):
            sum += img[i, j]
    return sum // (size * size)

# 获取骰子灰度图, 骰子size=(30,30)
def getDiceImg(path="") :
    if len(diceImg) <= 6:
        for i in range(1, 7) :
            diceImg.append(cv2.imread(os.getcwd() + f"/dicesDrawing/resources/dice{i}.jpg", 0))
            if diceImg[i] is None :
                print("找不到骰子图片")
                exit(0)
    return diceImg

def getDicesVideo(path, diceNumOfLine = 100) :
    # 获取输入视频的信息
    vedio_capture = cv2.VideoCapture(path)
    fps = vedio_capture.get(cv2.CAP_PROP_FPS) # 获取图像的帧，即该视频每秒有多少张图片
    frame_counter = int(vedio_capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数
    width = int(vedio_capture.get(cv2.CAP_PROP_FRAME_WIDTH)) # 获取图像的宽度和高度
    height = int(vedio_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print(fps, width, height)
    print(f"原视频帧数={fps}, 宽={width}, 高={height}, 骰子个数大小{height // 20} * {width // 20}")

    # 1.要创建的视频文件名称 2.编码器 3.帧率 4.size
    videoWrite = cv2.VideoWriter(path[:-4] + "_out.mp4", cv2.VideoWriter_fourcc(*'XVID'), fps, (1920, 1080))   
    
    ratio = frame_counter//44
    # 对原视频每一帧进行骰子画处理，合并为新视频
    # for i in tqdm.tqdm(range(0, frame_counter)):
    i = 0
    while vedio_capture.isOpened():
        # 读取每一帧，falg表示是否读取成功，frame为图片的内容
        (_, frame) = vedio_capture.read()   
        if frame is None:
            break
        # getDicesDrawing((width // 20, height // 20), frame, videoWrite)
        for n in range(100):
            if i == ratio * n:
                cv2.imwrite(f'_frame_{n}.jpg', frame)

        i += 1
    
    videoWrite.release()
    vedio_capture.release()
    print("getDicesVideo success!")
    return msgOk(f"原视频帧数={fps}, 宽={width}, 高={height}. 每一帧视频骰子个数 = {height // 20} * {width // 20}. 骰子动画的分辨率=1920*1080")


def getDicesDrawing(size, img, videoWrite) :
    # 图片大小即为骰子数目
    img = cv2.resize(img, size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 归一化
    cv2.normalize(img, img, 0, 255, cv2.NORM_MINMAX)
    
    height, width = img.shape
    diceNum = [[0 for _ in range(width)] for _ in range(height)]
    # print(f"图像的骰子规格为{len(diceNum)}*{len(diceNum[0])}")
    for i in range(len(diceNum)):
        for j in range(len(diceNum[i])):
            diceNum[i][j] = getDiceNum(getAveragePixel(img, i, j, 1))

    # 根据骰子点数 将骰子图片拼接起来
    diceImg = getDiceImg()  # 获取骰子图片
    imgOut = cv2.vconcat([cv2.hconcat([diceImg[num] for num in i]) for i in diceNum])
    imgOut = cv2.resize(imgOut, (1920, 1080))

    # 灰度图片转彩色图片，否则不能保存为视频
    imgOut = cv2.cvtColor(imgOut, cv2.COLOR_GRAY2BGR)
    videoWrite.write(imgOut)
    
    return msgOk([len(diceNum), len(diceNum[0])])

if __name__ == "__main__":
    # for i in range(1, 7) :
    #     # print(os.getcwd())
    #     diceImg.append(cv2.imread(os.getcwd() + f"/dicesDrawing/resources/dice{i}.jpg", 0))
    #     if diceImg[i] is None :
    #         print("找不到骰子图片")
    #         exit(0)
    #     print('骰子size=', diceImg[i].shape)
    getDicesVideo("./zhongli.mp4", 100)

