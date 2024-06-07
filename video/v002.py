import cv2
import numpy as np

cap = cv2.VideoCapture('../asset/C0068.mp4')

if not cap.isOpened():
    print('Cannot open video resource')
    exit()

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)

# 定义编译解码器并创建 VideoWriter 对象
# *'mp4v' 等价于 ('m', 'p', '4', 'v')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('../asset/test.mp4',
                      fourcc,
                      fps,
                      (int(width), int(height)),
                      True)

# 循环读取视频帧
while True:
    # 读取视频帧
    ret, frame = cap.read()
    # 使用 ret 判断是否读取到视频帧
    if ret is True:
        # 反转视频帧
        frame = cv2.flip(frame, 0)
        # 显示结果帧
        cv2.imshow('v002', frame)
        # 写入处理后的视频帧
        out.write(frame)
        c = cv2.waitKey(1) & 0xFF
        if c == ord('q'):
            break
    else:
        break


# 释放资源
# cao.release()
cap.release()
out.release()
cv2.destroyAllWindows()
