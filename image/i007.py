# 图像几何变换
import cv2 as cv
import numpy as np


# 缩放
img = cv.imread('../asset/test.png')
res = cv.resize(img, None, fx=2, fy=2, interpolation=cv.INTER_CUBIC)
height, width = res.shape[:2]
res = cv.resize(res, (2 * width, 2 * height), interpolation=cv.INTER_CUBIC)


# 平移
img1 = cv.imread('../asset/test.png', 0)
rows, cols = img1.shape
M = np.float32([[1, 0, 100], [0, 1, 50]])
# cv2.warpAffine()
# 仿射变换
# param1: 输入图像
# param2: 变换矩阵
# param3: 输出图像大小 (width, height) = (cols, rows)
dst = cv.warpAffine(img1, M, (cols, rows))
cv.imshow('img1', img1)
cv.imshow('dst', dst)
cv.waitKey(0)
cv.destroyAllWindows()


# 旋转
rows, cols, channels = img.shape
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
M = cv.getAffineTransform(pts1, pts2)
dst = cv.warpAffine(img, M, (cols, rows))
cv.imshow('dst1', dst)
cv.waitKey(0)
cv.destroyAllWindows()


# 透视变换
pts3 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
pts4 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
M = cv.getPerspectiveTransform(pts3, pts4)
dst = cv.warpPerspective(img, M, (300, 300))
cv.imshow('dst2', dst)
cv.waitKey(0)
cv.destroyAllWindows()
