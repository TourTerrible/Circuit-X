import cv2
import numpy as np
#red==1
lowerBound1=np.array([160,80,0])
upperBound1=np.array([179,255,255])
#green==2
lowerBound2=np.array([33,80,40])
upperBound2=np.array([90,255,255])
#blue==3
lowerBound3=np.array([100,90,0])
upperBound3=np.array([121,255,255])
#yellow==4
lowerBound4=np.array([20,100,100])
upperBound4=np.array([30,255,255])

def delete_repeated(coordinates_array_2d):
    final=[]
    flag=0
    flag2=0
    for a in coordinates_array_2d:
        if(flag==0):
            final.append(a)
            flag=1
        else:
            flag2=0
            for x in final:
                if((abs(x[0]-a[0])>20 ) or (abs(x[1]-a[1])>20 ) ):
                    continue
                else:
                    flag2=1
                    break
            if(flag2==0):
                    final.append(a)
    return(final)  

def find_output(img):
    bluredimg=cv2.GaussianBlur(img,(5,5),1)
    imgGRAY=cv2.cvtColor(bluredimg,cv2.COLOR_BGR2GRAY)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lowerBound4,upperBound4)
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
        x, y, w, h = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        
       
        #cv2.circle(img, (x,y), 5, (25,0,200), 2)
        #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
        cv2.drawContours(img,cnt,-1,(0,0,255),2)
        output_final_yellow=[x,y]
        print("yellow",output_final_yellow)
        return(output_final_yellow)
def find_input(img):
    
    bluredimg=cv2.GaussianBlur(img,(5,5),1)
    imgGRAY=cv2.cvtColor(bluredimg,cv2.COLOR_BGR2GRAY)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(imgHSV, lowerBound1,upperBound1)
    col_red = cv2.bitwise_and(img,img, mask= mask_red)
    maskGRAY=cv2.cvtColor(col_red,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_red, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    initial_input_red=[]
    initial_input_green=[]
    initial_input_blue=[]
           
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(area>0):
        	red_flag=1
        else:
            red_flag=0	
        x, y, w, h = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        
        
            #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
        cv2.drawContours(img,cnt,-1,(0,0,255),2)
        initial_input_red.append([x,y])
        print("red",[x,y])
    mask_green = cv2.inRange(imgHSV, lowerBound2,upperBound2)
    col_green = cv2.bitwise_and(img,img, mask= mask_green)
    maskGRAY=cv2.cvtColor(col_green,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_green, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(area>0):
        	green_flag=1
        else:
            green_flag=0
        x, y, w, h = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        
            #cv2.rectangle(img,(x-15,y-10op_x_y=[j[0],j[1]]
              
        cv2.drawContours(img,cnt,-1,(0,0,255),2)
        print("green",[x,y])
        initial_input_green.append([x,y])

    mask_blue = cv2.inRange(imgHSV, lowerBound3,upperBound3)
    col_blue = cv2.bitwise_and(img,img, mask= mask_blue)
    maskGRAY=cv2.cvtColor(col_blue,cv2.COLOR_BGR2GRAY)
    filtered = cv2.fastNlMeansDenoising(mask_blue, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        
            #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
        if(len(approx)>=7):  
            cv2.drawContours(img,cnt,-1,(0,0,255),2)
            initial_input_blue.append([x,y]) 
            print("blue",[x,y])   
    inputs=[initial_input_red,initial_input_green,initial_input_blue]
    return(inputs)
def findwires(img):


    coordinate_corner=[]
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
        x, y, w, h = cv2.boundingRect(cnt)
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        
        
        #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
        #cv2.drawContours(img,cnt,-1,(0,255,255),2)
        corners = cv2.goodFeaturesToTrack(maskGRAY, 25, 0.05, 10)
        #cv2.putText(img, str(len(approx))+"area"+str(area),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)

        #holes=getLandmarks(corners)
        for i in corners:
            x,y=i.ravel()
            x_y=[x,y]

            coordinate_corner.append(x_y)
            #cv2.circle(img, (x,y), 3, (255,255,0), 2)
#cv2.imshow("icole",col) 
    return(coordinate_corner)           
                #cv2.putText(img,str(len(approx)),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)





img =cv2.imread("test_circuit_2.jpg")

                
#print(str(len(approx))+"a"+str(perimeter))
#cv2.imshow("Blue",col)

find_output(img)
find_input(img)

#coordi=findwires(img)
#final_corner=delete_repeated(coordi)
#print((np.array(coordinate_corner)))
#print(np.shape(final_corner))
#print(delete_repeated(coordinate_corner))

#for i in final_corner:
	#cv2.circle(img, (i[0],i[1]), 5, (25,0,200), 2)
cv2.imshow("im",img)	






cv2.waitKey(0)