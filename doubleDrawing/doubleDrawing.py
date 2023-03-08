'''
双面画，输入两张图片，横向交叉合并成一张，
'''
import numpy as np
import cv2

def msgOk(msg):
    return [True, msg]

def msgErr(msg):
    return [False, msg]

def getDoubleDrawing(path1, path2, num):
    print(f"path1={path1}, path2={path2}, num={num}")
    # 处理输入图片，灰度并归一化
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None or img2 is None:
        print("找不到待处理图片")
        return msgErr("找不到待处理图片")
    
    # 通过等比例缩放 统一高度
    m1, n1, _ = img1.shape
    m2, n2, _ = img2.shape
    m = m1 if m1 > m2 else m2
    img1 = cv2.resize(img1, (m, m * n1 // m1))
    img2 = cv2.resize(img2, (m, m * n2 // m2))

    # 通过填补空白 统一宽度
    m1, n1, _ = img1.shape
    m2, n2, _ = img2.shape
    if (n1 - n2) // 2 > 0:
        empty_img = np.zeros((m2, (n1 - n2) // 2, 3), np.uint8)
        empty_img.fill(255)
        img2 = cv2.hconcat([empty_img, img2, empty_img])
    elif (n2 - n1) // 2 > 0:
        empty_img = np.zeros((m1, (n2 - n1) // 2, 3), np.uint8)
        empty_img.fill(255)
        img1 = cv2.hconcat([empty_img, img1, empty_img])

    # 每个图片分割成num份，拼接起来
    imgs = [] 
    m1, n1, _ = img1.shape
    m2, n2, _ = img2.shape
    empty_img = np.zeros((m1, 3, 3), np.uint8)  # 填充3像素宽度空白
    empty_img.fill(255)
    for i in range(num):
        imgs.append(img1[:, i * n1 // num : (i + 1) * n1 // num - 1, :])
        imgs.append(img2[:, i * n2 // num : (i + 1) * n2 // num - 1, :])
        imgs.append(empty_img)

    img_out = cv2.hconcat(imgs)
    cv2.imwrite(path1[:-4] + "_out.jpg", img_out)
    return

if __name__ == "__main__":
    getDoubleDrawing("./doubleDrawing/linghua.png", "./doubleDrawing/test.png", 10)