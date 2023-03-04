'''
点画
将原图像缩小之后，使用PIL中的convert('1')函数转换，即可实现
'''
from PIL import Image 
import numpy as np
import cv2

# 获得矩形的宽或高
def get_min_0_len(img, is_col):
    raw = 0
    col = 1
    if is_col == 1:
        raw = 1
        col = 0
        
    min_len = img.shape[0]
    for mm in range(img.shape[raw]):
        i = 0
        for nn in range(img.shape[col]):
            if img[mm, nn] == 0:
                i += 1
            else:
                if i != 0:
                    min_len = min(min_len, i)
                i = 0
    return min_len

# 将一个黑色矩形缩小为一个像素点，并淡化
def reset_point(img, ral_len, col_len, point_pixel = 180):
    for mm in range(img.shape[0]):
        for nn in range(img.shape[1]):
            if img[mm, nn] != 0:
                continue
            for i in range(ral_len):
                for j in range(col_len):
                    if mm + j < img.shape[0] and nn + col_len < img.shape[1]:
                        img[mm + j, nn + i] = 255
            if mm + ral_len // 2 < img.shape[0] and nn + col_len // 2 < img.shape[1]:
                img[mm + ral_len // 2, nn + col_len // 2] = point_pixel


# img = cv2.imread(orgimg, 0)
# img = cv2.resize(img, None, fx=0.1, fy=0.1)
# cv2.imwrite(out_path, img)


# ii= Image.open(out_path).convert('1')
# cv_img = cv2.cvtColor(np.asarray(ii), cv2.COLOR_RGB2BGR)
# cv2.imwrite(out_path, cv_img)

# ii.save("out2.jpg") 

def getPointDrawing(path, ratio = 1, point_pixel = 180, new_size = 100):
    pil_img = Image.open(path)
    m, n = pil_img.size
    # new_size = 100
    resize_pil_img = pil_img.resize((new_size, new_size * n // m))
    point_img = resize_pil_img.convert('1')

    resize_img2 = point_img.resize((ratio * m, ratio * n))
    resize_img2.save(path[:-4] + "_temp.jpg")

    # PIL图像转cv2图像
    cv_img = cv2.cvtColor(np.asarray(resize_img2.convert("L")), cv2.COLOR_BGR2BGRA)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # 将图像中的每个黑色矩形缩小为一个像素点，并淡化
    ral_len = get_min_0_len(cv_img, 0)
    col_len = get_min_0_len(cv_img, 1)
    reset_point(cv_img, ral_len, col_len, point_pixel)

    cv2.imwrite(path[:-4] + "_out.jpg", cv_img)
    return


if __name__ == "__main__":
    getPointDrawing("./pointDrawing/linghua.png", 2, 1, 70)