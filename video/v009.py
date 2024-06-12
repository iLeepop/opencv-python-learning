# TODO : 没有成功
# 使用异步加速
import cv2
import threading
from queue import Queue

# 打开视频流或摄像头

# 读取第一帧，初始化 KCF 跟踪器

# frame_queue = Queue(maxsize=10)
# 用于保存处理结果的队列
result_queue = Queue(maxsize=10)

cap = cv2.VideoCapture('../asset/worker-zone-detection.mp4')
if not cap.isOpened():
    print("Failed to open camera or video stream")
    exit()
ret, frame = cap.read()
if not ret:
    print("Failed to read frame for one")
    exit()
cv2.namedWindow("Tracking")
cv2.imshow("Tracking", frame)
# 手动选定初始跟踪目标
bbox = cv2.selectROI("Tracking", frame, False)


def track_object():
    global result_queue, frame, bbox

    # 创建 KCF 跟踪器
    tracker = cv2.TrackerKCF.create()
    tracker.init(frame, bbox)
    while True:
        if not cap.isOpened():
            print("Failed to open camera or video stream")
            break
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame for two")
            break
        # frame_queue.put(frame)
        ok, bbox = tracker.update(frame)
        result_queue.put((frame, ok, bbox))
        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def handle_results():
    global result_queue
    while True:
        print("队列是否为空：", result_queue.empty())
        if not result_queue.empty():
            print('开始处理')
            frame, ok, bbox = result_queue.get()
            # 绘制跟踪结果
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
            else:
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                            2)

            cv2.imshow("Tracking", frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# 启动处理结果的线程
to = threading.Thread(target=track_object)
to.start()
hr = threading.Thread(target=handle_results)
hr.start()


to.join()
hr.join()


# 释放资源
# cap.release()
# cv2.destroyAllWindows()
