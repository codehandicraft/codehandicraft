
import cv2
from cv2 import *

# file = 'yelan.jpg'
# img = cv2.imread('1.jpg', 0)
# # /home/msc/pythonCode/dicesDrawing/input/_D`BE6ZX1SF%85TCW{7TP9J.png
# print(img)
# print("----------------")

# cv2.imwrite("img.png",img)
# print("hello")



# 1\. 导入keyring模块
import keyring

# 2\. 设置密码
# 第一个参数为: 应用名(指定在哪一个应用中来使用)
# 第二个参数为: 用户名
# 第三个参数为: 密码
keyring.set_password('smtp.qq.com', '1421204127@qq.com', 'ugtbmkmrxlysjdgh')

# 3\. 获取密码
# 第一个参数为: 应用名(指定在哪一个应用中来使用)
# 第二个参数为: 用户名
my_password = keyring.get_password('system', '1421204127@qq.com')
print(my_password)

