import cv2
import numpy as np

lowerBound3=np.array([100,90,0])
upperBound3=np.array([121,255,255])

def resize(imgsaved,img_extracted):

    img_new=np.ones((52,73,3),dtype=int)
    for i in range(0,52):
        img_new[i]=np.append(img[i],[img[i][71]],axis=0)

    return(img_new)

def find_wires_corner(img):
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
        
        if(len(approx)):
            #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
            cv2.drawContours(img,cnt,-1,(0,255,255),2)
            corners = cv2.goodFeaturesToTrack(maskGRAY, 25, 0.05, 10)

            #holes=getLandmarks(corners)
            for i in corners:
                x,y=i.ravel()
                x_y=[x,y]

                coordinate_corner.append(x_y)
                #cv2.circle(img, (x,y), 3, (255,255,0), 2)
    #cv2.imshow("image",img) 
    return(coordinate_corner) 

def count_gate_n_type(array_2d_final):
    #count=[not,and,or,xnor,xor,nor,nand]
    count_gate=[0,0,0,0,0,0,0]
    for a in array_2d_final:
        if(a[4]==0):
            count_gate[0]=count_gate[0]+1
        if(a[4]==1):
            count_gate[1]=count_gate[1]+1
        if(a[4]==2):
            count_gate[2]=count_gate[2]+1
        if(a[4]==3):
            count_gate[3]=count_gate[3]+1
        if(a[4]==4):
            count_gate[4]=count_gate[4]+1
        if(a[4]==5):
            count_gate[5]=count_gate[5]+1
        if(a[4]==6):
            count_gate[6]=count_gate[6]+1                

    return(count_gate)    


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
                if((abs(x[0]-a[0])>3 ) or (abs(x[1]-a[1])>3 ) ):
                    continue
                else:
                    flag2=1
                    break
            if(flag2==0):
                    final.append(a)
    return(final)

def delete_repeated_wire_corners(coordinates_array_2d):
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
                if((abs(x[0]-a[0])>30 ) or (abs(x[1]-a[1])>10 ) ):
                    continue
                else:
                    flag2=1
                    break
            if(flag2==0):
                    final.append(a)
    return(final)                        

def detect_not(img):
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
    filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 50, 50)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
             

    i=0
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(perimeter>80 and perimeter<130 and area>10): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            #cv2.drawContours(img,cnt,-1,(0,255,255),2)
            #print(area,"pr",perimeter,"len",len(approx))
            if(len(approx)>=2 and len(approx)<=5):
                
                #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
                print(area,"pr",perimeter,"len",len(approx))
                cv2.putText(img, "NOT",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1) 
                return(1)  

def dot_detect(img):
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
    filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours

    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(area>20 and area <30): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            
            if(len(approx)>=6):
                #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
                cv2.drawContours(img,cnt,-1,(0,255,255),2)
                #cv2.putText(img, str(area)+"p"+str(perimeter),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)

            #print("w" ,len(approx),area,perimeter)
                #print(str(area)+"p"+str(perimeter)+"l"+str(len(approx)))
                return(1)

def curve_detect(img):
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
    filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours

    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)
        if(perimeter>20 and perimeter<600 and area<100 and area>50): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            
            if(len(approx)<=8 ):
            #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
                cv2.drawContours(img,cnt,-1,(0,255,255),2)

            #print("w" ,len(approx),area,perimeter)
                #print(str(area)+"p"+str(perimeter)+"l"+str(len(approx)))
                return(1)
                

def identify_gates(img):
    
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
    filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
    edges = cv2.Canny(filtered, 80, 80)
    _, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
             

    i=0
    for cnt in contours_all:
        perimeter = cv2.arcLength(cnt,True)
        area= cv2.contourArea(cnt)

        if(area>150 and perimeter<600): 
            
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            if(len(approx)>=5):
                cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
                cv2.putText(img, str(area),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                cv2.drawContours(img,cnt,-1,(0,255,255),2)
                
                #curve_detect(img[y-10:y+h+10,x-13:x+w+13])
                #dot_detect(img[y-10:y+h+10,x-13:x+w+13])
                print(np.shape(img[y-10:y+h+10,x-10:x+w+13]))
                #print(np.shape(or_saved))
                #img[y-10:y+h+10,x-10:x+w+13]=cv2.resize(img[y-10:y+h+10,x-10:x+w+13],(72,52),interpolation=cv2.INTER_LINEAR)
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(and_saved)):

                    #print("enter_and")
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-and_saved)==0 ):
                        #print("subtracted")
                        if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):
                            t=6
                            values=[x,y,w,h,t]
                            coordinates.append(values)
                            cv2.putText(img, "NAND",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                        else:
                            t=1
                            values=[x,y,w,h,t]
                            coordinates.append(values)
                            cv2.putText(img, "AND",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)  
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(or_saved)):
                    #print("enter_or")
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-or_saved)==0 ):
                        if(curve_detect(img[y-10:y+h+10,x-13:x+w+13])):
                            if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):
                                t=3
                                values=[x,y,w,h,t]
                                coordinates.append(values)
                                cv2.putText(img, "XNOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                            else:
                                t=4
                                values=[x,y,w,h,t]
                                coordinates.append(values)
                                cv2.putText(img, "XOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)        
                        else:
                            if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):
                                t=5
                                values=[x,y,w,h,t]
                                coordinates.append(values)
                                cv2.putText(img, "NOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                            else:
                                t=2
                                values=[x,y,w,h,t]
                                coordinates.append(values)
                                cv2.putText(img, "OR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
        if(perimeter>80 and perimeter<130 and area>10): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            #cv2.drawContours(img,cnt,-1,(0,255,255),2)
            #print(area,"pr",perimeter,"len",len(approx))
            if(len(approx)>=2 and len(approx)<=5):
                t=0
                values=[x,y,w,h,t]
                coordinates.append(values)
                #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
                print(area,"pr",perimeter,"len",len(approx))
                cv2.putText(img, "NOT",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1) 
                
                
                


img=cv2.imread("test_circuit_0.jpg")
or_saved=cv2.imread("img_main0.png")
and_saved=cv2.imread("img_main9.png")
#and_saved=resize(and_saved)


coordinates=[]
identify_gates(img)
final_corner=delete_repeated_wire_corners(find_wires_corner(img))
print(np.array(final_corner))
for i in final_corner:
    cv2.circle(img, (i[0],i[1]), 5, (25,0,200), 2)

print(delete_repeated(coordinates))
print("number of gates:", np.shape(delete_repeated(coordinates))[0])
print(count_gate_n_type(delete_repeated(coordinates)))
print("[NOT,AND,OR,XNOR,XOR,NOR,NAND]")





            
#cv2.imshow("edges",edges) 
cv2.imshow("1",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()                 