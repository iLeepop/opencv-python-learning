import cv2
import numpy as np

# cv2.imread()
# param1: 图片文件路径
# param2: 模式
#   cv2.IMREAD_COLOR: 彩色图 (默认) 1
#   cv2.IMREAD_GRAYSCALE: 灰度图 0
#   cv2.IMREAD_UNCHANGED: 原图包括 alpha 通道 -1
img = cv2.imread('../asset/test.png', -1)

# cv2.imshow()
# param1: 窗口名
# param2: 显示的图片对象
cv2.imshow('i001', img)

# 键盘绑定函数
# 如果在一段时间内触发了指定按键，程序将继续运行
k = cv2.waitKey(0) & 0xFF
if k == 27:
    # 销毁所有窗口
    cv2.destroyAllWindows()
    # or cv2.destroyWindow('i001') 消除特定窗口
elif k == ord('s'):
    # 保存图片
    # cv2.imwrite()
    # param1: 保存路径
    # param2: 图片对象
    cv2.imwrite('../asset/test_save.png', img)
    cv2.destroyAllWindows()

# 额外内容 Matplotlib 绘图库

