import time

import cv2

model_bin = "../model/face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel"
config_text = "../model/face_detector/deploy.prototxt"

model_bin1 = "../model/face_detector/res_ssd_300Dim.caffeModel"
config_text1 = "../model/face_detector/weights-prototxt.txt"

# 加载 caffe 模型
net = cv2.dnn.readNetFromCaffe(config_text1, model_bin1)

# 设置 back-end
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# 设置 rtsp 地址
rtsp_url = "rtsp://admin:abc12345@192.168.1.40:554/Streaming/Channels/301"

# GStreamer pipeline 结构
gst_pipeline = f"rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink"

# 使用 OpenCV 打开 GStreamer 管道
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

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
    ret, image = cap.read()
    if ret is False:
        break
    # 人脸检测
    h, w = image.shape[:2]
    blobImage = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    net.setInput(blobImage)
    cvOut = net.forward()

    # Put efficiency information.
    t, _ = net.getPerfProfile()
    fps = 1000 / (t * 1000.0 / cv2.getTickFrequency())
    label = 'FPS: %.2f' % fps
    cv2.putText(image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    # 绘制检测矩形
    for detection in cvOut[0, 0, :, :]:
        # 获取置信度
        score = float(detection[2])
        # 获取类别 (如果有对应的类名
        objIndex = int(detection[1])
        if score > 0.5:
            # 获取左上角坐标的 x
            left = detection[3]*w
            # 获取左上角坐标的 y
            top = detection[4]*h
            # 获取右下角坐标的 x
            right = detection[5]*w
            # 获取右下角坐标的 y
            bottom = detection[6]*h

            # 绘制目标区域
            # cv2.rectangle()
            # param1: 左上角坐标
            # param2: 右下角坐标
            cv2.rectangle(image, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), thickness=2)
            cv2.putText(image, "score:%.2f"%score, (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow('face-detection-demo', image)
    writer.write(image)
    c = cv2.waitKey(1)
    if c == 27:
        break
cv2.waitKey(0)
cap.release()
writer.release()
cv2.destroyAllWindows()