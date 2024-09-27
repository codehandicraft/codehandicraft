# import cv2
# import numpy as np

# # 读取图像
# image = 255-cv2.imread('in.jpg', cv2.IMREAD_GRAYSCALE)

# # 应用阈值，将图像转换为二值图
# _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# # 执行连通组件分析
# num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
# print(f"Number of labels: {num_labels}")
# print(f"Label stats: {stats}")
# print(f"Label centroids: {centroids}")

# # 创建一个空白图像用于绘制结果
# output_image = np.zeros_like(image)

# # 估计单个像素块的平均大小
# estimated_block_size = np.median(stats[1:, cv2.CC_STAT_AREA])
# print(f"Estimated block size: {estimated_block_size}")

# # 遍历所有的连通组件
# for i in range(1, num_labels):  # 0 label is for the background
#     # 获取连通组件的大小
#     size = stats[i, cv2.CC_STAT_AREA]
    
#     # 获取连通组件的bounding box
#     x, y, w, h, area = stats[i]
#     print(f"Label {i}: size={size}, x={x}, y={y}, w={w}, h={h}, area={area}")
    
#     # 提取连通区域
#     component_mask = (labels == i).astype(np.uint8) * 255
    
#     # 基于连通组件大小相对于预计的单个块大小进行分割决策
#     num_blocks_estimate = int(round(size / estimated_block_size))
#     print(f"Number of blocks estimate: {num_blocks_estimate}")
    
#     if num_blocks_estimate > 1:
#         print("Splitting component into blocks")
#         # 使用形态学操作尝试分割连通组件
#         # 例如，通过迭代腐蚀和膨胀操作来分离组件
#         eroded = cv2.erode(component_mask, np.ones((3, 3), np.uint8), iterations=1)
#         dilated = cv2.dilate(eroded, np.ones((3, 3), np.uint8), iterations=1)
        
#         # 将处理后的组件放回到输出图像中
#         output_image[y:y+h, x:x+w] = cv2.bitwise_or(output_image[y:y+h, x:x+w], dilated)

#     else:
#         # 如果只有一个块，则直接复制到输出图像
#         output_image[y:y+h, x:x+w] = cv2.bitwise_or(output_image[y:y+h, x:x+w], component_mask)

# # 显示原始图像和处理后的图像
# cv2.imshow('Original Image', 255-image)
# cv2.imshow('Output Image', 255-output_image)

# # 保存处理后的图像
# cv2.imwrite('separated_pixel_blocks.png', 255-output_image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np
from scipy.stats import mode


def should_skip_component(component_mask):
    # 计算黑色和白色像素的数量
    white_pixels = np.sum(component_mask == 255)
    black_pixels = np.sum(component_mask == 0)
    
    # 计算黑白像素比率
    # 为避免除以零的错误，我们添加一个小的常数epsilon
    epsilon = 1e-10
    # ratio = white_pixels / (black_pixels + epsilon)
    ratio = black_pixels / (white_pixels + epsilon)
    
    # 如果黑白像素比率接近1，我们选择跳过这个组件
    if ratio > 2:  # 这里的阈值可以根据实际需要进行调整
        return True
    else:
        return False
    
def remove_blocks_heuristic(image, block_size, step):
    # 用于保存结果的空白图像
    output = np.zeros_like(image)
    print(f"block_size: {block_size}, image.shape: {image.shape}, step: {step}")
    cv2.imwrite('put1.jpg', 255-image)

    # 遍历图像的每个像素
    x_first_set = False
    for y in range(0, image.shape[0], block_size):
        if y+block_size > image.shape[0]:
            continue
        enable_set_255 = x_first_set == False
        for x in range(0, image.shape[1], block_size):
            if x+block_size > image.shape[1]:
                continue
            # 根据步长决定是否保留当前小方块
            if should_skip_component(image[y:y+block_size, x:x+block_size]):
                enable_set_255 = True
                continue
            if enable_set_255:
                # output[y:y+block_size, x:x+block_size] = image[y:y+block_size, x:x+block_size]
                output[y:y+block_size, x:x+block_size] = 255
                if x == 0:
                    x_first_set = True
                enable_set_255 = False
                continue
            
            if enable_set_255 == False:
                enable_set_255 = True
                continue
            if x == 0:
                x_first_set = False
                continue



            # if (x // block_size + y // block_size) % step != 0:
            #     # 将小方块复制到输出图像中
            #     # output[y:y+block_size, x:x+block_size] = image[y:y+block_size, x:x+block_size]
            #     output[y:y+block_size, x:x+block_size] = 255
    cv2.imwrite('put2.jpg', 255-output)
    return output

# 读取图像
image = 255-cv2.imread('in.jpg', cv2.IMREAD_GRAYSCALE)  # 替换为你的图片文件名

# 应用阈值，将图像转换为二值图
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# 执行连通组件分析
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
print(f"num_labels: {num_labels}")
print(f"labels: {labels}")
print(f"stats: {stats}")
print(f"centroids: {centroids}")

# 估计单个小方块的尺寸
# 使用除背景外的所有连通组件的平均面积
# avg_area = np.mean(stats[1:, cv2.CC_STAT_AREA])
# print(f"avg_area: {avg_area}")
# block_size = int(np.sqrt(avg_area))  # 假设方块是正方形
# print(f"block_size: {block_size}")
# 获取所有连通组件的面积，并计算众数
areas = stats[1:, cv2.CC_STAT_AREA]  # 排除背景的面积
# most_common_area = mode(areas)[0][0]
most_common_area = np.median(stats[1:, cv2.CC_STAT_AREA])
block_size = int(np.sqrt(most_common_area))  # 假设方块是正方形

# 分割步长，这里假设每隔一个方块删除一个，即步长为2
step = 2

# 用于保存分割后结果的图像
separated_image = np.zeros_like(binary_image)

cnt = 0
# 遍历所有的连通组件
for i in range(1, num_labels):  # 跳过0标签，因为它代表背景
    # 获取连通组件的大小
    size = stats[i, cv2.CC_STAT_AREA]
    # 获取连通组件的bounding box
    x, y, w, h, area = stats[i]
    print(f"Label {i}: x={x}, y={y}, w={w}, h={h}, area={area}, avg_area={most_common_area}")

    # 提取连通区域
    component_mask = (labels == i).astype(np.uint8) * 255
    component_image = binary_image[y:y+h, x:x+w]

        
    # 基于连通组件大小相对于预计的单个块大小进行分割决策
    # num_blocks_estimate = int(round(size / most_common_area))
    num_blocks_estimate = int((size / most_common_area))
    
    if num_blocks_estimate > 1:
        print(f"Number of blocks estimate: {num_blocks_estimate}")
        
        # 将处理后的组件放回到输出图像中
        # separated_image[y:y+h, x:x+w] = cv2.bitwise_or(separated_image[y:y+h, x:x+w], dilated)
        separated_component = remove_blocks_heuristic(component_image, block_size, step)
        separated_image[y:y+h, x:x+w] = cv2.bitwise_or(separated_image[y:y+h, x:x+w], separated_component)
        if num_blocks_estimate>9:
            break
        # if cnt >= 3:
        #     break
        cnt += 1    


    else:
        # 如果只有一个块，则直接复制到输出图像
        separated_image[y:y+h, x:x+w] = cv2.bitwise_or(separated_image[y:y+h, x:x+w], component_image)
    
    # 分割连通组件
    # separated_component = remove_blocks_heuristic(component_image, block_size, step)
    
    # # 将处理后的组件放回到分割后结果图像中
    # separated_image[y:y+h, x:x+w] = cv2.bitwise_or(separated_image[y:y+h, x:x+w], separated_component)

# # 显示原始图像和处理后的图像
# cv2.imshow('Original Image', 255-image)
# cv2.imshow('Separated Blocks', 255-separated_image)

# # 等待按键后关闭窗口
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 保存处理后的图像
cv2.imwrite('separated_blocks.png', 255-separated_image)