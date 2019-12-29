
import cv2
import numpy as np

lowerBound3=np.array([100,200,0])
upperBound3=np.array([121,255,255])
img=cv2.imread("or_not_and_c.jpg")

bluredimg=cv2.GaussianBlur(img,(5,5),1)
imgGRAY=cv2.cvtColor(bluredimg,cv2.COLOR_BGR2GRAY)
imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
mask = cv2.inRange(imgHSV, lowerBound3,upperBound3)
col = cv2.bitwise_and(img,img, mask= mask)
maskGRAY=cv2.cvtColor(col,cv2.COLOR_BGR2GRAY)


filtered = cv2.fastNlMeansDenoising(mask, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 80, 80)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
       # find countours around chips, see image: contours
#cv2.drawContours(img,contours_all[4],-1,(0,255,255),2)
for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    if(area>0 or perimeter>0 ):
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)   
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(img, str(len(approx))+"area"+str(area),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1) 
        print(str(len(approx))+"area"+str(area))




cv2.imshow("2",mask)
cv2.imshow("1",img)

#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()  
