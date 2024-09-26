import cv2
import numpy as np

def color_quantization(image, k):
    # 将图像转换为数据
    data = np.float32(image).reshape((-1, 3))

    # 定义终止条件 (类型, 最大迭代次数, 移动的最小距离)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    # 应用K-Means算法
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # 将中心转换为uint8类型
    center = np.uint8(center)

    # 映射颜色中心回原始图像像素
    result = center[label.flatten()]
    result_image = result.reshape((image.shape))

    return result_image

# 读取图像
img = cv2.imread('ly.jpg')

# 设置要使用的颜色数量
k = 4  # 例如，将图像分割成4种颜色

# 应用色彩量化算法
quantized_image = color_quantization(img, k)

# 显示结果
cv2.imshow('Original Image', img)
cv2.imshow('Quantized Image', quantized_image)
cv2.imwrite('quantized_image.jpg', quantized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()