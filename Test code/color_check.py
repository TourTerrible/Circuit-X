import cv2
import numpy as np
#red==1
lowerBound1=np.array([0,80,0])
upperBound1=np.array([10,255,255])
#green==2
lowerBound2=np.array([33,80,40])
upperBound2=np.array([90,255,255])
#blue==3
lowerBound3=np.array([100,115,0])
upperBound3=np.array([121,255,255])
#yellow==4
lowerBound4=np.array([20,100,100])
upperBound4=np.array([30,255,255])

def return_red_green_flag(img):

    red_flag=0
    green_flag=0
    yellow_flag=0
    bluredimg=cv2.GaussianBlur(img,(5,5),1)
    imgGRAY=cv2.cvtColor(bluredimg,cv2.COLOR_BGR2GRAY)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(imgHSV, lowerBound1,upperBound1)
    col_red = cv2.bitwise_and(img,img, mask= mask_red)
    maskGRAY=cv2.cvtColor(col_red,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_red, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

           
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if(area>0):
            cv2.drawContours(img,cnt,-1,(0,0,255),2)
            cv2.putText(img,"red",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
            red_flag=1
         
        
    mask_green = cv2.inRange(imgHSV, lowerBound2,upperBound2)
    col_green = cv2.bitwise_and(img,img, mask= mask_green)
    maskGRAY=cv2.cvtColor(col_green,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_green, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if(area>0 or perimeter>0 ):
            cv2.drawContours(img,cnt,-1,(0,255,255),2)
            cv2.putText(img,"green",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
            green_flag=1

    mask_yellow = cv2.inRange(imgHSV, lowerBound4,upperBound4)
    col_yellow = cv2.bitwise_and(img,img, mask= mask_yellow)
    maskGRAY=cv2.cvtColor(col_yellow,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_yellow, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(area>0 or perimeter>0 ):
            yellow_flag=1        
        
        

    return([red_flag,green_flag,yellow_flag])


img=cv2.imread("test_1.jpg")
print(return_red_green_flag(img))    
cv2.imshow("1",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()    