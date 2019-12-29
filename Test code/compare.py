import cv2
import numpy as np
img=cv2.imread("sample4.png")

img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 80, 80)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours

for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    if(perimeter<150 and area>100): 
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
        x, y, w, h = cv2.boundingRect(cnt)
        
        if(len(approx)==8):
	        #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
	        cv2.drawContours(img,cnt,-1,(0,255,255),2)
	        #print("w" ,len(approx),area,perimeter)
	        print("yes x")
	        
	           


cv2.imshow("dsa",img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
