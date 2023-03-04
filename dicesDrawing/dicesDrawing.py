import cv2 as cv
import xlwt
import numpy as np
import os

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

# 获取骰子灰度图
def getDiceImg(path) :
    diceImg = [0,]
    for i in range(1, 7) :
        diceImg.append(cv.imread(os.getcwd() + f"/dicesDrawing/resources/dice{i}.jpg", 0))
        if diceImg[i] is None :
            print("找不到骰子图片")
            return []
            # return msgErr("找不到骰子图片")
    return diceImg

def getDicesDrawing(path, diceNumOfLine = 100) :
    # path = os.getcwd() + "/dicesDrawing/input/" + path
    img = cv.imread(path, 0)
    if (img is None):
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    # cv.imwrite(path[:-4] + "_gray.jpg", img)
    
    # 归一化
    cv.normalize(img, img, 0, 255, cv.NORM_MINMAX)
    # cv.imwrite(path[:-4] + "_norm.jpg", img)
    
    # 将图像剪切为diceSize最大整数倍
    img_height, img_width = img.shape
    diceSize = img_height // diceNumOfLine
    if diceSize < 1:
        diceSize = 1
    # imgRoi = img[img_height % diceSize // 2 : img_height - img_height % diceSize // 2, img_width % diceSize // 2 : img_width - img_width % diceSize // 2]
    imgRoi = img[img_height % diceNumOfLine // 2 : img_height - img_height % diceNumOfLine // 2, img_width % diceNumOfLine // 2 : img_width - img_width % diceNumOfLine // 2]
    
    # 根据图像计算所有骰子点数
    # 并且保存骰子画点数分布到xls表中
    dicesDrawingXls = xlwt.Workbook(encoding='utf-8')
    sheet=dicesDrawingXls.add_sheet('dice number')
    height, width = imgRoi.shape
    diceNum = [[0 for _ in range(width // diceSize)] for _ in range(height // diceSize)]
    for i in range(len(diceNum)):
        for j in range(len(diceNum[i])):
            diceNum[i][j] = getDiceNum(getAveragePixel(imgRoi, i * diceSize, j * diceSize, diceSize))
            sheet.write(i,j,diceNum[i][j])
    dicesDrawingXls.save(path[:-4] + "_out.xls")

    # 根据骰子点数 将骰子图片拼接起来
    diceImg = getDiceImg(path)  # 获取骰子图片
    # 将diceNum中的点数替换成对应点数的骰子图片，组合成骰子画
    # imgLines = []
    # for i in diceNum:
    #     matLines = []
    #     for num in i:
    #         matLines.append(diceImg[num])
    #     imgLines.append(cv.vconcat(matLines))
    # imgOut = cv.hconcat(imgLines)
    imgOut = cv.vconcat([cv.hconcat([diceImg[num] for num in i]) for i in diceNum])
    
    # 保存输出图片
    cv.imwrite(path[:-4] + "_out.jpg", imgOut)
    return msgOk([len(diceNum), len(diceNum[0])])

if __name__ == "__main__":
    getDicesDrawing("dicesDrawing/input/1.jpg", 100)

