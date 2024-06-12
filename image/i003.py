import cv2
import numpy as np


drawing = False
mode = True
ix, iy = -1, -1


# 定义鼠标回调函数
def draw_circle(event, x, y, flags, param):
    global  drawing, mode, ix, iy
    # 鼠标左键按下
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        # 记录鼠标按下时的坐标
        ix, iy = x, y
    # 鼠标移动
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
            else:
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
    # 鼠标左键松开
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), -1)
        else:
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
    # 鼠标左键双击
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        if mode:
            cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
    # 鼠标右键按下
    elif event == cv2.EVENT_RBUTTONDOWN:
        mode = not mode


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while(1):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()
