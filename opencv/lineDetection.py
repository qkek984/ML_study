#-*- coding: cp949 -*-
#-*- coding: utf-8 -*-

import cv2
import numpy as np
import random
I=0

origin = cv2.imread('c.jpg')
#cv2.imshow('Origin',origin)
img = cv2.cvtColor(origin, cv2.COLOR_RGB2GRAY)
#img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.Canny(img, 30,150, apertureSize=3)
cv2.imshow('canny',img)

##-----find rectangle
(_,contours, _) = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
tmp=[]
for cnt in contours:
    if cv2.contourArea( cnt)> 2000:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            cv2.drawContours(origin, [approx],-1,(0,0,255),8)
            #print (approx)
            tmp.append(approx)
x=[]
y=[]
for v in tmp:
    v= np.reshape(v,(4,2))
    print v
    for tx in v:
        x.append(tx[0])
        y.append(tx[1])
    #print max(y)
    maxX,maxY,minX,minY= max(x),max(y),min(x),min(y)
    print max(x),max(y),min(x),min(y)
    print ("###########")
    x = []
    y = []

##############################################
lines = cv2.HoughLinesP(img,1,1*np.pi/180,20,np.array([]),100,5)

#----------find gradient
lines = np.squeeze(lines)
#vertical
slope_degree= (np.arctan2(lines[:,1] - lines[:,3], lines[:,0] - lines[:,2]) * 180) / np.pi
#limit 1
lines1 = lines[np.abs(slope_degree)<95]
slope_degree = slope_degree[np.abs(slope_degree)<95]
#limit 2
lines1 = lines1[np.abs(slope_degree)>85]
slope_degree = slope_degree[np.abs(slope_degree)>85]

lines1 = lines1[(slope_degree>0),:]

lines1 = lines1[:,None]

for line in lines1:
    #print line
    #print ("---------")
    for x1,y1,x2,y2 in line:
        cv2.line(origin,(x1,y1), (x2,y2), (255,0,0),2)
    #cv2.putText(origin,str(I),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    I=I+1
# horizontal
slope_degree2= (np.arctan2(lines[:,1] - lines[:,3], lines[:,0] - lines[:,2]) * 180) / np.pi
#limit 1
lines2 = lines[np.abs(slope_degree2)<181]
slope_degree2 = slope_degree2[np.abs(slope_degree2)<181]
#limit 2
lines2 = lines2[np.abs(slope_degree2)>=179]
slope_degree2 = slope_degree2[np.abs(slope_degree2)>179]

lines2 = lines2[(slope_degree2>0),:]

lines2 = lines2[:,None]

I=0
for line in lines2:
    for x1,y1,x2,y2 in line:
        cv2.line(origin,(x1,y1), (x2,y2), (255,0,0),2)
    #cv2.putText(origin,str(I),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
    I=I+1


#temp= np.zeros((origin.shape[0],origin.shape[1],3),dtype=np.uint8)
#temp = np.copy(origin) * 0
#result = cv2.addWeighted(origin, 1, temp,1,0)
#origin = cv2.resize(origin, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
cv2.imshow('Result',origin)

cv2.waitKey(0)
cv2.destroyAllWindows()
