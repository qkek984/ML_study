import cv2
import numpy as np

def EdgeTracking(origin, img):
    (_, contours, _) = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 2000:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:##-----find rectangle
                cv2.drawContours(origin, [approx],-1,(0,0,255),2)

origin = cv2.imread('c.jpg')
img = cv2.cvtColor(origin, cv2.COLOR_RGB2GRAY)
img = cv2.Canny(img, 30,150, apertureSize=3)
cv2.imshow('canny',img)
EdgeTracking(origin,img)
cv2.imshow('Result',origin)

cv2.waitKey(0)
cv2.destroyAllWindows()