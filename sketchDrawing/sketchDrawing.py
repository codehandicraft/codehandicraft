'''
线稿画
参考：https://blog.csdn.net/xiangxueerfei/article/details/127750980?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-127750980-blog-122724653.pc_relevant_3mothn_strategy_recovery&spm=1001.2101.3001.4242.1&utm_relevant_index=3
'''
import cv2
#读取图片
image = cv2.imread("linghua.png")
#将BGR图像转换为灰度
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#图像反转
inverted_image = 255 - gray_image

blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
inverted_blurred = 255 - blurred
pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

cv2.imwrite("out2.jpg", pencil_sketch)