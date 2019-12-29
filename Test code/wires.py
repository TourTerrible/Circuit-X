import cv2
import numpy as np

#red==1
lowerBound1=np.array([160,100,100])
upperBound1=np.array([179,255,255])
#green==2
lowerBound2=np.array([33,80,40])
upperBound2=np.array([90,255,255])
#blue==3
lowerBound3=np.array([100,150,0])
upperBound3=np.array([121,255,255])
#yellow==4
lowerBound4=np.array([20,100,100])
upperBound4=np.array([30,255,255])

def findcolor(color,img):
	bluredimg=cv2.GaussianBlur(img,(5,5),1)
    imgGRAY=cv2.cvtColor(bluredimg,cv2.COLOR_BGR2GRAY)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    if color==3:
        mask = cv2.inRange(imgHSV, lowerBound3,upperBound3)
        col = cv2.bitwise_and(img,img, mask= mask)
        
       
        filtered = cv2.fastNlMeansDenoising(mask, 8, 8, 7, 21)
        edges = cv2.Canny(filtered, 80, 80)
        _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours
        #cv2.drawContours(img,contours_all[4],-1,(0,255,255),2)
        for cnt in contours_all:


            perimeter = cv2.arcLength(cnt,True)
            area= cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
            if(area<5):
	            if(len(approx)):
	                cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
	                cv2.drawContours(img,cnt,-1,(0,255,255),2)
	                cv2.putText(img,str(len(approx)),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
	                cv2.imshow("image",img)
	                print(str(len(approx))+"a"+str(perimeter))
	                cv2.imshow("Blue",col)

img =cv2.imread("and_or_2.png")

findcolor(3,img)
cv2.waitKey(0)
cv2.destroyAllWindows()