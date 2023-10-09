'''
双面画，输入两张图片，横向交叉合并成一张，
'''
import cv2
import sys
sys.path.append("../")
import util
import os
import math
from pointDrawing import pointDrawing
from reflexDrawing import reflexDrawing

def crop_img(img1, h, w):
    print(f"crop_img: img_shape={img1.shape[:2]}, h={h}, w={w}")
    h = int(h * 100)
    w = int(w * 100)
    gcd = math.gcd(h, w)
    h //= gcd
    w //= gcd
    img1_new_h = min(img1.shape[0] // h, img1.shape[1] // w) * h
    img1_new_w = min(img1.shape[0] // h, img1.shape[1] // w) * w
    img1 = img1[(img1.shape[0]-img1_new_h)//2: (img1.shape[0]-img1_new_h)//2 + img1_new_h, (img1.shape[1]-img1_new_w)//2: (img1.shape[1]-img1_new_w)//2 + img1_new_w]
    print(f"crop_img: img_shape={img1.shape[:2]}, gcd_h={h}, gcd_w={w}")
    return img1

def split_img_w(img1, num):
    split_img1 = []
    split_width = img1.shape[1]//(num)
    for i in range(num):
        split_img1.append(img1[:, i*split_width:(i+1)*split_width, :])
    return split_img1

def getDragonScaleBinding(input_file_list, param_int_list):
# def getDragonScaleBinding(path1, path2, h, w, cover, num):
    """
    获取DragonScale Binding所需的图片。
    
    Args:
        path1 (str): 正面图片路径。
        path2 (str): 背面图片路径。
        h (int): 图片高度。
        w (int): 图片宽度。
        cover (int): 封面数量。
        num (int): 其他数量。
    
    Returns:
        None
    """
    # parse parmas
    try:
        path1 = input_file_list[0]
        path2 = input_file_list[1]
        # default param 30, 68, 34, 10
        h = 30
        w = 68
        split_num = 34
        cover_num = 10
        is_singl_img = 0
        is_fill_blank_img = 0
        if len(param_int_list) < 4:
            print("parma num < 4, use default param")
        else:
            h = param_int_list[0]
            w = param_int_list[1]
            split_num = param_int_list[2]
            cover_num = param_int_list[3]
            if len(param_int_list) > 4:
                is_singl_img = param_int_list[4]
            if len(param_int_list) > 5:
                is_fill_blank_img = param_int_list[5]
    except Exception as e:
        print(f"parse param error: {e}")
        return util.msgErr(f"{e}")
    contetn_split_num = split_num - cover_num
    # split_num切分个数，cover_num封面暂用个数，contetn_split_num内容个数（实际内容的页数为=contetn_split_num-1）
    print(f"input_file_list num = {len(input_file_list)}, path1={path1}, path2={path2}, h={h}, w={w}, split_num={split_num}, cover_num={cover_num}, contetn_split_num={contetn_split_num}, is_singl_img={is_singl_img}")

    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None or img2 is None:
        print("找不到待处理图片")
        return util.msgErr("找不到待处理图片")
    # height, width = img.shape[:2]
    print(f"before img1's shape:{img1.shape}, img2's shape:{img2.shape}")
    img1 = crop_img(img1, h, w)
    img2 = crop_img(img2, h, w)
    print(f"after  img1's shape:{img1.shape}, img2's shape:{img2.shape}")

    # 通过等比例缩放 统一高度
    m1, n1, _ = img1.shape
    m2, n2, _ = img2.shape
    m = m1 if m1 > m2 else m2
    img1 = cv2.resize(img1, (m * n1 // m1, m))
    img2 = cv2.resize(img2, (m * n2 // m2, m))
    ratio = img1.shape[0] // h
    print(f"统一高度 ok, {img1.shape}, {img2.shape}, ratio={ratio}")
    util.imwrite(path1, '_crop', img1)
    util.imwrite(path2, '_crop', img2)

    height, width = img1.shape[:2]
    split_width = img1.shape[1]//(split_num)
    print(f"split width = {split_width}, {split_width/ratio}")

    # 切分封面
    split_img1 = split_img_w(img1, split_num)
    cover_img1 = cv2.hconcat(split_img1[:cover_num])
    other_img1 = split_img1[cover_num:]
    util.imwrite(path1, '_split_cover', cover_img1)
    print(f"other_img1 size = {len(other_img1)}")
    # TODO 视频需要
    # TODO 视频需要
    # fill_img = util.get_empty_img((height, split_width//5, 3)) # TODO 视频需要
    # split_img_all = []# TODO 视频需要
    # for i in range(len(split_img1)):
    #     text_img = cv2.putText(split_img1[i], str(i+1), (0, height//20), cv2.FONT_HERSHEY_SIMPLEX, 6, (0,0,255), 25)
    #     split_img_all.append(text_img)
    #     if i != len(split_img1)-1:
    #         split_img_all.append(fill_img)
    #     util.imwrite(path1, f'_split_{i}', split_img1[i])  # TODO 视频需要
    # util.imwrite(path1, '_split_all',  cv2.hconcat(split_img_all))
    # cover_other_img = split_img_all[2*cover_num-2:]
    # cover_other_img[0] = cover_img1
    # util.imwrite(path1, '_split_cover_all',  cv2.hconcat(cover_other_img))
    print("split img1 ok")

    # 切分背面 
    split_img2 = split_img_w(img2, split_num)
    cover_img2 = cv2.hconcat(split_img2[contetn_split_num:-1])    #第二张图片即背面封面少一个分片
    other_img2 = split_img2[:contetn_split_num]
    util.imwrite(path2, '_crop_cover', cover_img2)
    util.imwrite(path2, '_crop_0', other_img2[0])
    print(f"other_img2 size = {len(other_img2)}")
    # TODO 视频需要
    # fill_img = util.get_empty_img((height, split_width//5, 3)) # TODO 视频需要
    # split_img_all = []# TODO 视频需要
    # for i in range(len(other_img2)):
    #     text_img = cv2.putText(other_img2[i], str(i+1), (0, height//20), cv2.FONT_HERSHEY_SIMPLEX, 6, (0,0,255), 25)
    #     split_img_all.append(text_img)
    #     split_img_all.append(fill_img)
    #     util.imwrite(path2, f'_split_{i}', split_img2[i])  # TODO 视频需要
    # util.imwrite(path2, '_split_all',  cv2.hconcat(split_img_all))
    # split_img_all.append(cover_img2)
    # cover_other_img = split_img_all
    # util.imwrite(path2, '_split_cover_all',  cv2.hconcat(cover_other_img))
    print("split img2 ok")

    empty_img = util.get_empty_img((height, split_width, 3))
    # page_img_1 = cv2.hconcat([empty_img, cover_img1, other_img1[0], other_img2[0], content_img])
    # print(f"page_img_1's shape:{page_img_1.shape}")
    # util.imwrite(path1, 'page_img_1', page_img_1)

    # 暂时用空白图片作为内容（TODO）
    content_imgs = []
    print(f"height={height}, width={split_width*(2*cover_num-1)}")
    # for i in range(1, 60):
    for content_path in input_file_list:
        if content_path == path1 or content_path == path2:
            continue
        # path = f"frame/_frame_{i}.jpg"
        content_img = cv2.imread(content_path)
        if content_img is None:
            print(f"imread error: {content_path}, use empty img")
            content_img = util.get_empty_img((height, split_width*(2*cover_num-1), 3))
            # return util.msgErr(f"找不到待处理图片{content_path}") 
        print(f"{content_path} origion shape={content_img.shape}")
        # 统一宽高比例
        if is_fill_blank_img:
            content_img = util.unify_h_w_ratio_by_fill_blank(content_img, h, (w/(split_num))*(2*cover_num-1))
        else:
            content_img = crop_img(content_img, h, (w/(split_num))*(2*cover_num-1))
        print(f"{content_path} after   shape={content_img.shape}")
        # 通过等比例缩放 统一高度
        m1, n1, _ = content_img.shape
        m2, n2, _ = img2.shape
        # m = m1 if m1 < m2 else m2
        m = m2
        content_img = cv2.resize(content_img, (m * n1 // m1, m))
        # img2 = cv2.resize(img2, (m * n2 // m2, m))
        ratio = content_img.shape[0] // h
        print(f"统一高度 ok, {content_img.shape}, {img2.shape}, ratio={ratio}")
        content_imgs.append(content_img)
    print(f"get content img num = {len(content_imgs)}")
    empty_img_num = contetn_split_num - 1 - len(content_imgs)
    for i in range(empty_img_num):
        content_imgs.append(util.get_empty_img((height, split_width*(2*cover_num-1), 3)))
    print(f"add empty img, get content img num = {len(content_imgs)}")
        
    # content_img_wider = util.get_empty_img(cover_img1.shape)
    # content_img_narrower = util.get_empty_img((height, split_width*(cover_num-1), 3))
    # print(f"content_img_wider shape:{content_img_wider.shape}, content_img_narrower shape:{content_img_narrower.shape}")
    # print(f"内容图片的尺寸cm : {content_img_wider.shape[0]/ratio} * {(content_img_wider.shape[1] + content_img_narrower.shape[1])/ratio}")
    print(f"内容图片的尺寸cm : {content_imgs[0].shape[0]/ratio} * {(content_imgs[0].shape[1])/ratio}")

    # 集合封面和内容  [cover1(t+1), t, t+1, t, t+1, t, t+1 cover2(t)]
    content_img_list = [cover_img1]
    for i in range(contetn_split_num - 1):
        # 一窄一宽刚好相邻，可以组成左右页，所有像素点都不会被遮挡
        content_img_list.append(content_imgs[i][:,:split_width*(cover_num-1),:])
        # TODO 视频需要
        # util.imwrite(path1, f'_content_{i}_0', content_img_list[-1])
        content_img_list.append(content_imgs[i][:,split_width*(cover_num-1):,:])
        # util.imwrite(path1, f'_content_{i}_1', content_img_list[-1])
        # content_img_list.append(content_img_narrower)
        # content_img_list.append(content_img_wider)
    content_img_list.append(cover_img2)

    # 拼接图片
    out_path_list = []
    page_img_list = []
    img_size_cm = []
    dst_h = 300
    for i in range(contetn_split_num):
        page_img = cv2.hconcat([content_img_list[2 * i], other_img1[i], other_img2[i], content_img_list[2 * i + 1]])
        # 双面打印逻辑
        if is_singl_img != 0:
            page_img = cv2.hconcat([content_img_list[2 * i], other_img1[i]])
            page_img2 = cv2.hconcat([other_img2[i], content_img_list[2 * i + 1], util.get_empty_img((height, split_width, 3))])
            # page_img2 画点，用于区分粘贴部分 
            for j in range(6):
                cv2.circle(page_img2, (page_img2.shape[1]-split_width, page_img2.shape[0]//5*j), 3, 0, -1)
            # print(page_img.shape, page_img2.shape)
        if i == 0:
            img_size_cm = [page_img.shape[0]/ratio, page_img.shape[1]/ratio]
            print(f"拼接图片的尺寸cm : {page_img.shape[0]/ratio} * {(page_img.shape[1])/ratio}")
        out_path_list.append(util.imwrite(path1, f'_page_img_{i}', page_img))
        page_img_list.append(util.resize_img(page_img, dst_h))
        # 双面打印逻辑
        if is_singl_img != 0:
            out_path_list.append(util.imwrite(path1, f'_page_img_{i}_back', page_img2))
            page_img_list.append(util.resize_img(page_img2, dst_h))
    print("page img save ok")

    out_img = cv2.hconcat(page_img_list)
    out_path_list.append(util.imwrite(path1, f'_page_out', out_img))
    if not os.path.exists(out_path_list[-1]):
        print(f"保存图片失败，{out_path_list[-1]}")
        out_path_list = out_path_list[:-1]
    else:
        print("page out img save ok")

    print([img_size_cm, out_path_list, [h,w,split_num,cover_num,is_singl_img,is_fill_blank_img]])
    return util.msgOk([img_size_cm, out_path_list, [h,w,split_num,cover_num,is_singl_img,is_fill_blank_img]])


if __name__ == "__main__":
    input_path_list = ['./zhongli/0.jpg', './zhongli/1.png']
    input_path_list = ['./input/20231007204728_636_966957/0.jpg', './input/20231007204728_636_966957/1.jpg']
    input_para_list = [10, 26, 12, 3]
    # ['27', '32', '34', '10']
    # input_para_list = [27,32,34,10]
    # plain= ['10', '135', '45', '20']
    # input_para_list = [int(param) for param in plain]
    for i in range(30):
        path = f"./zhongli/_frame_{i}.jpg"
        path = f"./input/20231007204728_636_966957/{i}.jpg"
        content_img = cv2.imread(path)
        if content_img is None:
            continue
        input_path_list.append(path)

    getDragonScaleBinding(input_path_list, input_para_list)
