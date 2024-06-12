# 图像算术运算
import cv2
import numpy as np


img1 = cv2.imread('../asset/splash.png')
img2 = cv2.imread('../asset/test.png')
# 图形大小不一致需要调整
img1 = cv2.resize(img1, (100, 100), fx=0.5, fy=0.5)
img2 = cv2.resize(img2, (1000, 1000), fx=0.5, fy=0.5)
dts = cv2.addWeighted(img2[0:100, 0:100], 0.7, img1, 0.3, 0)
img2[0:100, 0:100] = dts

rows, cols, channels = img1.shape
roi = img2[0:rows, 0:cols]
# 创建 logo 的掩码与其相反掩码
img1gary = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img1gary, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# 将 ROI 中 logo 部分区域涂黑
img2_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
# 提取 logo 部分
img1_fg = cv2.bitwise_and(img1, img1, mask=mask)
# 将 logo 放入 ROI 并修改主图像
dst = cv2.add(img2_bg, img1_fg)
img2[0:rows, 0:cols] = dst
cv2.imshow('dts', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
