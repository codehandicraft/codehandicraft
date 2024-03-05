'''
双面画，输入两张图片，横向交叉合并成一张，
'''
import numpy as np
import cv2
import sys
sys.path.append("../")
import util
from reflexDrawing import reflexDrawing
from pointDrawing import pointDrawing

def getDoubleDrawing(path1, path2, num):
    """
    将两张图片路径和分割份数作为参数，得到拼接后的图片
    
    Args:
        path1 (str): 第一张图片的路径
        path2 (str): 第二张图片的路径
        num (int): 分割的份数
    
    Returns:
        Tuple[bool, np.ndarray]: 返回一个元组，第一个元素为bool类型，表示拼接是否成功，第二个元素为np.ndarray类型，表示拼接后的图片
    
    """
    print(f"normal img path1={path1}, reflex img path2={path2}, num={num}")

    # 处理第二张图片，得到反射画
    # ret = reflexDrawing.getReflexDrawing(path2, 180)
    # if ret[0] == False:
    #     print("getReflexDrawing falied")
    #     return util.msgErr("获取反射画失败")
    reflex_img_path = path2
    # # out_path = util.imwrite(reflex_img_path, '_reflex', img_out)

    # 处理输入图片，灰度并归一化
    normal_img = cv2.imread(path1)
    # reflex_img = cv2.imread(path2)
    reflex_img = cv2.imread(reflex_img_path)
    if normal_img is None or reflex_img is None:
        print("找不到待处理图片")
        return util.msgErr("找不到待处理图片")
    reflex_img = util.crop_white_border(reflex_img)
    normal_img = util.crop_empty(normal_img)
    print(f"图片灰度 ok, {normal_img.shape}, {reflex_img.shape}")

    normal_img = cv2.rotate(normal_img, cv2.ROTATE_90_CLOCKWISE)
    # reflex_img = cv2.rotate(reflex_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    print(f"图片旋转 ok, {normal_img.shape}, {reflex_img.shape}")

    # 通过等比例缩放 统一高度
    m1, n1, _ = normal_img.shape
    m2, n2, _ = reflex_img.shape
    m = m1 if m1 > m2 else m2
    normal_img = cv2.resize(normal_img, (m * n1 // m1, m))
    reflex_img = cv2.resize(reflex_img, (m * n2 // m2, m))
    print(f"统一高度 ok, {normal_img.shape}, {reflex_img.shape}")

    normal_img = util.crop_empty(normal_img)
    reflex_img = util.crop_empty(reflex_img)
    util.imwrite(path1, '_normal_crop', normal_img)
    util.imwrite(path2, '_reflex_crop', reflex_img)

    # normal在左侧，reflex在右侧
    # 通过填补空白 统一宽度
    m1, n1, _ = normal_img.shape
    m2, n2, _ = reflex_img.shape
    if (n1 - n2) // 2 > 0:
        empty_img = np.zeros((m2, (n1 - n2) // 2, 3), np.uint8)
        empty_img.fill(255)
        # reflex在右侧，reflex的空白全部补充到左侧
        reflex_img = cv2.hconcat([empty_img, empty_img, reflex_img])
    elif (n2 - n1) // 2 > 0:
        empty_img = np.zeros((m1, (n2 - n1) // 2, 3), np.uint8)
        empty_img.fill(255)
        normal_img = cv2.hconcat([empty_img, normal_img, empty_img])
    print(f"统一宽度 ok, {normal_img.shape}, {reflex_img.shape}")

    util.imwrite(path1, '_normal', normal_img)
    util.imwrite(path2, '_reflex', reflex_img)

    # 每个图片分割成num份，拼接起来
    imgs = [] 
    m1, n1, _ = normal_img.shape
    m2, n2, _ = reflex_img.shape
    empty_img = np.zeros((m1, 20, 3), np.uint8)  # 填充像素宽度空白
    empty_img.fill(255)
    util.imwrite(path1, f"_empty", empty_img)
    for i in range(num):
        y_ratio1 = 1 + (i / num)
        img1 = normal_img[:, i * n1 // num : (i + 1) * n1 // num - 1, :]
        img1 = cv2.resize(img1, None, fx=1, fy=y_ratio1)
        imgs.append(img1)
        util.imwrite(path1, f"_{i}", img1)
        imgs.append(empty_img)

        y_ratio2 = 1 + 1 - (i / num)
        img2 = reflex_img[:, i * n2 // num : (i + 1) * n2 // num - 1, :]
        img2 = cv2.resize(img2, None, fx=1, fy=y_ratio2)
        imgs.append(img2)
        util.imwrite(path2, f"_{i}", img2)
        if i != num -1:
            imgs.append(empty_img)
    
    # 通过填充空白统一宽高
    imgs = util.unify_size_h(imgs)
    print(f"统一尺寸 ok, {imgs[0].shape}")

    img_out = cv2.hconcat(imgs)
    out_path = util.imwrite(path1, '_out', img_out)
    print(f"完成拼接 ok, {img_out.shape}, out_path={out_path}")

    dst_img = util.under_pixel_to_dst(img_out, 240, 240)
    out_path = util.imwrite(path1, '_week', dst_img)
    return

if __name__ == "__main__":
    # getDoubleDrawing("./1.jpg", "./2.jpg", 10)
    getDoubleDrawing("./hh1.jpg", "./hh2_reflex.jpg", 15)