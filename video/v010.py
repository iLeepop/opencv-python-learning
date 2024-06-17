# 识别加追踪
import cv2 as cv
import numpy as np


model_bin = "../model/ssd/MobileNetSSD_deploy.caffemodel"
config_text = "../model/ssd/MobileNetSSD_deploy.prototxt"
objName = ["background",
           "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair",
           "cow", "diningtable", "dog", "horse",
           "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]
net = cv.dnn.readNetFromCaffe(config_text, model_bin)


# rtsp_url = 'rtsp://admin:abc12345@192.168.1.40:554/Streaming/Channels/101'
# gst_pipeline = f'rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink'
gst_pipeline = '../asset/soccer.mp4'
cap = cv.VideoCapture(gst_pipeline, cv.CAP_GSTREAMER)
# cap = cv.VideoCapture(0)

global cvOut
global bbox
global isTracking
global tracker


def create_tracker():
    return cv.TrackerKCF_create()


def detect_object(frame0):
    print("识别目标")
    global cvOut
    blob_image = cv.dnn.blobFromImage(frame0, 0.007843, (300, 300), (127.5, 127.5, 127.5), True, False)
    net.setInput(blob_image)
    cvOut = net.forward()


def process_frame(frame0):
    print("处理目标框选")
    global cvOut, bbox, isTracking
    h, w = frame0.shape[:2]
    for detection in cvOut[0, 0, :, :]:
        score = float(detection[2])
        obj_index = int(detection[1])
        # 只筛选出置信度大于0.3 并且类别为15(人) 的目标
        if score > 0.3 and obj_index == 15:
            left = detection[3] * w
            top = detection[4] * h
            right = detection[5] * w
            bottom = detection[6] * h

            # 绘制
            cv.rectangle(frame0, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), thickness=2)
            # 跟踪区域太大导致帧率下降
            # if not isTracking and int(right - left) <= 100 and int(bottom - top) <= 100:
            # 只跟踪人
            if not isTracking and int(right - left) <= 300 and int(bottom - top) <= 300:
                bbox = (int(left), int(top), int(right - left), int(bottom - top))
                tracker.init(frame, bbox)
                isTracking = True
            break


def track_object(frame0):
    print("跟踪目标")
    global isTracking, tracker
    # t, _ = net.getPerfProfile()
    # fps = 1000 / (t * 1000.0 / cv.getTickFrequency())
    # print("FPS: {:.2f}".format(fps))
    ok, b = tracker.update(frame0)
    if ok:
        p1 = (int(b[0]), int(b[1]))
        p2 = (int(b[0] + b[2]), int(b[1] + b[3]))
        cv.rectangle(frame0, p1, p2, (0, 0, 255), 2, 1)
    # 根据FPS判断跟踪状态
    # elif fps < 27:
    #     print("因帧率过低，停止跟踪")
    #     isTracking = False
    #     tracker = create_tracker()
    else:
        print("跟踪失败，停止跟踪")
        isTracking = False
        tracker = create_tracker()


if __name__ == '__main__':
    isTracking = False
    tracker = create_tracker()
    cv.waitKey(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if not isTracking:
            detect_object(frame)
            process_frame(frame)
        else:
            track_object(frame)
        cv.imshow("frame", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

