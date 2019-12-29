import cv2
import numpy as np

            

img=cv2.imread("test_circuit_1.jpg")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 50, 50)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
         

i=0
for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    if(perimeter>80 and perimeter<200 and area>10 and area <600): 
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(img,cnt,-1,(0,255,255),2)
        print(area,"pr",perimeter,"len",len(approx))
        if(len(approx)>=2 and len(approx)<=6):
	        
	        cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
	        print(area,"pr",perimeter,"len",len(approx))
	        

cv2.imshow("dsa",img)
cv2.waitKey(0)
cv2.destroyAllWindows()