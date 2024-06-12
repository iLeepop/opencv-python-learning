# 使用 MobileNetSSD 检测
import cv2

model_bin = "../model/ssd/MobileNetSSD_deploy.caffemodel"
config_text = "../model/ssd/MobileNetSSD_deploy.prototxt"
objName = ["background",
           "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair",
           "cow", "diningtable", "dog", "horse",
           "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]

# load caffe model
net = cv2.dnn.readNetFromCaffe(config_text, model_bin)

# 设置 rtsp 地址
rtsp_url = "rtsp://admin:abc12345@192.168.1.40:554/Streaming/Channels/301"

# GStreamer pipeline 结构
gst_pipeline = f"rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink"

# 检测
# cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture('../asset/worker-zone-detection.mp4')
# 跳帧
should_jump = 10
cvOut = None
jump_frame = should_jump


def process_frame(frame0):
    global cvOut, jump_frame
    # h, w = frame.shape[:2]
    for detection in cvOut[0, 0, :, :]:
        score = float(detection[2])
        obj_index = int(detection[1])
        if score > 0.3:
            left = detection[3] * w
            top = detection[4] * h
            right = detection[5] * w
            bottom = detection[6] * h

            # 绘制
            cv2.rectangle(frame0, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), thickness=2)
            cv2.putText(frame0, "score:%.2f, %s" % (score, objName[obj_index]),
                        (int(left) - 10, int(top) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, 8)


while True:
    ret, frame = cap.read()
    if ret is False:
        break

    h, w = frame.shape[:2]
    if jump_frame == should_jump:
        blobImage = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), True, False)
        net.setInput(blobImage)
        cvOut = net.forward()
        process_frame(frame)
        jump_frame = 0
    else:
        if cvOut is not None:
            process_frame(frame)
            jump_frame += 1
    cv2.imshow('video-ssd-demo', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
