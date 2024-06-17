# 使用跟踪
import cv2
import numpy as np


# rtsp_url = 'rtsp://admin:abc12345@192.168.1.40:554/Streaming/Channels/101'
# gst_pipeline = f'rtspsrc location={rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink'
gst_pipeline = '../asset/worker-zone-detection.mp4'


global img
global isTracking
global ok
global bbox
global p1, p2, rect




def draw_range(event, x, y, flags, param):
    global img, p1, p2, rect, isTracking
    if event == cv2.EVENT_LBUTTONDOWN:
        isTracking = False
        p1 = (x, y)
        cv2.imshow('Tracking', img)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
        cv2.rectangle(img, p1, (x, y), (0, 255, 0), 2)
        cv2.imshow('Tracking', img)
    elif event == cv2.EVENT_LBUTTONUP:
        p2 = (x, y)
        cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
        cv2.imshow('Tracking', img)
        if p1 != p2:
            min_x = min(p1[0], p2[0])
            min_y = min(p1[1], p2[1])
            width = abs(p1[0] - p2[0])
            height = abs(p1[1] - p2[1])

            bbox = (min_x, min_y, width, height)
            tracker.init(frame, bbox)
            isTracking = True


if __name__ == '__main__':
    tracker = cv2.TrackerCSRT_create()
    isTracking = False
    cv2.namedWindow('Tracking')
    # cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening video stream or file")
        exit(1)

    jump_frame = 6
    now_frame = jump_frame

    while True:
        cv2.setMouseCallback('Tracking', draw_range)
        ret, frame = cap.read()
        if not ret:
            break
        img = frame
        timer = cv2.getTickCount()
        if isTracking and now_frame == jump_frame:
            ok, bbox = tracker.update(frame)
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
            else:
                print('Tracking failure detected')
                isTracking = False
                tracker = cv2.TrackerCSRT.create()
            now_frame = 0
        elif isTracking:
            now_frame += 1
            if isTracking:
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
        cv2.imshow('Tracking', frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
