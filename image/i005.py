import time

import cv2
import numpy as np


img = cv2.imread('../asset/test.png')
# 访问像素点
pixel = img[0, 0]
# 打印像素点信息 [B, G, R]
print(pixel)
# 仅打印 blue 像素信息
print(pixel[0])
# 使用 numpy 访问
RED = img.item(10, 10, 2)
# 修改 RED 值
img.itemset((10, 10, 2), 100)
_RED = img.item(10, 10, 2)
print(_RED)

# 访问图像形状
shape = img.shape
# 返回行，列，通道数的元组 (行, 列, 通道数) (如果图片为彩色
print(shape)
# 如果图像是灰度的 则不返回通道数

# 访问像素总数
size = img.size
print(size)

# 图像数据类型
dtype = img.dtype
print(dtype)

# 图像ROI
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball

# 拆分图像
b, g, r = cv2.split(img)
_b = img[:, :, 0]
# 合并图像
img = cv2.merge((b, g, r))
# 设置特定像素为 0
img[:, :, 1] = 0

cv2.imshow('image', img)
cv2.imwrite(f'test_out{time.time()}.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

