# 图像阈值
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


img = cv.imread('../asset/test.png', 0)
ret, thresh11 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, thresh12 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
ret, thresh13 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
ret, thresh14 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
ret, thresh15 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
imgs = [img, thresh11, thresh12, thresh13, thresh14, thresh15]
for i in range(6):
    plt.subplot(2, 3, i + 1), plt.imshow(imgs[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()


