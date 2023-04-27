'''
线稿画
参考：https://blog.csdn.net/xiangxueerfei/article/details/127750980?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-127750980-blog-122724653.pc_relevant_3mothn_strategy_recovery&spm=1001.2101.3001.4242.1&utm_relevant_index=3
'''
import cv2
import numpy as np

def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
    image = cv2.filter2D(image, -1, kernel=kernel)

    # # 使用拉普拉斯滤波进行锐化处理
    # laplacian = cv2.Laplacian(image, cv2.CV_64F)

    # # 将锐化后的图像与原图像进行加权融合，增强锐化效果
    # image = cv2.addWeighted(image, 1.5, laplacian, -0.5, 0, image)

    cv2.imwrite("_out.jpg", image)
    return image

#读取图片
image = cv2.imread("naxida2.jpg")
#将BGR图像转换为灰度
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#图像反转
inverted_image = 255 - gray_image

blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
inverted_blurred = 255 - blurred
pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

# pencil_sketch = custom_blur_demo(pencil_sketch)
cv2.imwrite("out1.jpg", pencil_sketch)