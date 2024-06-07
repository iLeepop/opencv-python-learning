import time
import cv2
import numpy as np


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 设置 rtsp 地址
rtsp_url = "rtsp://admin:abc12345@192.168.1.40:554/Streaming/Channels/301"

# GStreamer pipeline 结构
gst_pipeline = f"rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink"

# 使用 OpenCV 打开 GStreamer 管道
# cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture('../asset/C0057.mp4')

if not cap.isOpened():
    print("Error opening video stream or file")
    exit(0)

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(f"./output-{time.time()}.mp4", fourcc, fps, (int(width), int(height)), True)

# cap = cv2.VideoCapture('C:/Users/Administrator/Desktop/C0057.mp4')
while True:
    ret, frame = cap.read()
    if ret is False:
        break
    # 人脸检测
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8), padding=(32, 32), scale=1.05)
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)

    writer.write(frame.astype('uint8'))
    cv2.imshow("frame", frame)
    # 绘制检测矩形
    c = cv2.waitKey(1)
    if c == 27:
        break


cv2.waitKey(0)
cap.release()
writer.release()
cv2.destroyAllWindows()