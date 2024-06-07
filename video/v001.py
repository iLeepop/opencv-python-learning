import cv2
import numpy as np

# 获取视频
# cv2.VideoCapture()
# param1: 0表示打开笔记本的内置摄像头，1表示打开外置摄像头，也可以传入视频文件的路径，或者视频流以及 gstreamer 的 pipeline
cap = cv2.VideoCapture('C:/Users/Administrator/Desktop/C0057.mp4')

# 判断视频是否打开
# cap.isOpened()
if not cap.isOpened():
    print('Cannot open video resource')
    exit()

# 循环读取视频帧
while True:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # 读取视频帧
    ret, frame = cap.read()
    # 使用 ret 判断是否读取到视频帧
    if not ret:
        print('Cannot read video resource')
        break
    # 将视频帧转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    # 显示结果帧
    cv2.imshow('v001', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
# cao.release()
cap.release()
cv2.destroyAllWindows()
