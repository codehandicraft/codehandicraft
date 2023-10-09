'''
线稿画，远近
参考：https://www.cnblogs.com/xingchong/p/15153488.html
'''

from PIL import Image 
import numpy as np
import cv2
import sys
sys.path.append("../")
import util

orgimg = 'li.jpg'
outimg = 'li_out.jpg'
a = np.asarray(Image.open(orgimg).convert('L')).astype('float')

ii= Image.open(orgimg).convert('1')
ii.save("li_1.jpg") 
# img = cv2.cvtColor(ii, cv2.COLOR_RGB2BGR)
# cv2.imwrite("01.jpg", img)

# 根据灰度变化来模拟人类视觉的明暗程度
depth = 10.             # 预设虚拟深度值为10 范围为0-100 
grad = np.gradient(a)   # 提取梯度值
grad_x, grad_y = grad   # 提取x y方向梯度值 解构赋给grad_x, grad_y

# 利用像素之间的梯度值和虚拟深度值对图像进行重构
grad_x = grad_x * depth / 100.
grad_y = grad_y * depth / 100. #根据深度调整x y方向梯度值

# 梯度归一化 定义z深度为1.  将三个梯度绝对值转化为相对值，在三维中是相对于斜对角线A的值
A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
uni_x = grad_x / A 
uni_y = grad_y / A 
uni_z = 1./ A

# 令三维中是相对于斜对角线的值为1
vec_el = np.pi / 2.1                    # 光源俯视角度   弧度值  接近90度
vec_az = np.pi / 4.                     # 光源方位角度   弧度值  45度
dx = np.cos(vec_el) * np.cos(vec_az)    # 光源对x轴的影响 对角线在x轴投影
dy = np.cos(vec_el) * np.sin(vec_az)    # 光源对y轴的影响 对角线在y轴投影
dz = np.sin(vec_el)                     # 光源对z轴的影响 对角线在z轴投影

b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z) # 光源归一化
b = b.clip(0, 255)                               # 为了避免数据越界，生成灰度值限制在0-255区间
im = Image.fromarray(b.astype('uint8'))         # 图像更构 
im.save(outimg)       # 保存图片

print("under to dst")
img = cv2.imread(outimg, 0)
img = util.under_pixel_to_dst(img, 200, 0)
cv2.imwrite("li_under_pixel.jpg", img)