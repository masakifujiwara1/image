import numpy as np
import cv2
from matplotlib import pyplot as plt
#
img = cv2.imread('choki.JPG', 0)
blur = cv2.GaussianBlur(img,(5,5),0)
ret1,th1 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

contours = cv2.findContours(
            th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
contours = list(filter(lambda x: cv2.contourArea(x) <= 1260000, contours))
max_cnt = max(contours, key=lambda x: cv2.contourArea(x))
out = np.zeros_like(th1)
cv2.drawContours(out, [max_cnt], -1, color=255, thickness=-1)
#print(type(img))
## ——–> <class ‘numpy.ndarray’>
#
#cv2.imshow("img", th1)
#k = cv2.waitKey( 0 )
#if k== 27:
#    cv2.destroyAllWindows()
#elif k == ord('s'):
#    cv2.imwrite('hand_two.png', img)
#    cv2.destroyAllWindows()
plt.imshow(out, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.show()
