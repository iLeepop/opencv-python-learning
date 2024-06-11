# opencv 绘图
import cv2
import numpy as np

# 创建一个黑色画布对象
img = np.zeros((512, 512, 3), np.uint8)

# 绘制一条对角线
# cv2.line()
# 参数1：画布对象
# 参数2：起点坐标
# 参数3：终点坐标
# 参数4：颜色
# 参数5：线宽
cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)

# 绘制矩形
# cv2.rectangle()
# 参数1：画布对象
# 参数2：左上角坐标
# 参数3：右下角坐标
# 参数4：颜色
# 参数5：线宽
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)

# 绘制圆形
# cv2.circle()
# 参数1：画布对象
# 参数2：圆心坐标
# 参数3：半径
# 参数4：颜色
# 参数5：线宽
cv2.circle(img, (447, 63), 63, (0, 0, 255), 3)

# 绘制椭圆
# cv2.ellipse()
# 参数1：画布对象
# 参数2：圆心坐标
# 参数3：长轴和短轴长度
# 参数4：旋转角度
# 参数5：开始角度
# 参数6：结束角度
# 参数7：颜色
# 参数8：线宽
cv2.ellipse(img, (256, 256), (100, 50), 0, 0, 300, 255, 3)

# 绘制多边形
pts = np.array([[10, 5], [200, 60], [100, 70], [50, 100]], np.int32)
pts = pts.reshape((-1, 1, 2))
# cv2.polylines()
# 参数1：画布对象
# 参数2：多边形顶点坐标
# 参数3：是否闭合
# 参数4：颜色
# 参数5：线宽
cv2.polylines(img, [pts], True, (0, 255, 255), 3)

# 绘制文字
font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText()
# 参数1：画布对象
# 参数2：文字内容
# 参数3：文字左上角坐标
# 参数4：字体
# 参数5：字体大小
# 参数6：颜色
# 参数7：线宽
# 参数8：字体样式
cv2.putText(img, "By ilee", (10, 500), font, 4, (0, 255, 255), 2, cv2.LINE_AA)

cv2.imshow("line", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
