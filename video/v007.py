# 颜色空间
import cv2
import numpy as np


cap = cv2.VideoCapture('../asset/worker-zone-detection.mp4')
if not cap.isOpened():
    print('Error opening video stream or file')
    exit(0)
while 1:
    ret, frame = cap.read()
    if not ret:
        break
    # 转换为HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 定义 HSV 中蓝色的范围
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # 设置 HSV 的阈值使得只取蓝色
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # 将掩膜和图像逐像素相加
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
