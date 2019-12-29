import cv2
import numpy as np

def resize(img):
    img_new=np.ones((52,73,3),dtype=int)
    for i in range(0,52):
        img_new[i]=np.append(img[i],[img[i][71]],axis=0)

    return(img_new)

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
                coordinates=[x,y,w,h]
                #curve_detect(img[y-10:y+h+10,x-13:x+w+13])
                #dot_detect(img[y-10:y+h+10,x-13:x+w+13])
                #print(np.shape(img[y-10:y+h+10,x-10:x+w+13]))
                #print(np.shape(or_saved))
                #img[y-10:y+h+10,x-10:x+w+13]=cv2.resize(img[y-10:y+h+10,x-10:x+w+13],(72,52),interpolation=cv2.INTER_LINEAR)
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(and_saved)):

                    print("enter_and")
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-and_saved)==0 ):
                        print("subtracted")
                        if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):
                            cv2.putText(img, "NAND",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                        else:
                            cv2.putText(img, "AND",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)  
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(or_saved)):
                    print("enter_or")
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-or_saved)==0 ):
                        if(curve_detect(img[y-10:y+h+10,x-13:x+w+13])):
                            if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):

                                cv2.putText(img, "XNOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                            else:
                                cv2.putText(img, "XOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)        
                        else:
                            if(dot_detect(img[y-10:y+h+10,x-13:x+w+13])):

                                cv2.putText(img, "NOR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                            else:
                                cv2.putText(img, "OR",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)

                
                


img=cv2.imread("test_circuit_1.jpg")
or_saved=cv2.imread("img_main0.png")
and_saved=cv2.imread("img_main9.png")
#and_saved=resize(an_saved)


identify_gates(img)

            
#cv2.imshow("edges",edges) 
cv2.imshow("1",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()                 