import cv2
import numpy as np

def detect_circle(img):
	img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
	filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
	edges = cv2.Canny(filtered, 80, 80)
	_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	               # find countours around chips, see image: contours

	for cnt in contours_all:
	    perimeter = cv2.arcLength(cnt,True)
	    area= cv2.contourArea(cnt)
	    if(area>20 and area <50): 
	        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
	        x, y, w, h = cv2.boundingRect(cnt)
	        if(len(approx)==10 or len(approx)==8):
	            #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
	            #print("circle detected" ,len(approx))
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
	    if(perimeter<150 and area>100): 
	        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
	        x, y, w, h = cv2.boundingRect(cnt)
	        
	        if(len(approx)<=8):
		        #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
		        #cv2.drawContours(img,cnt,-1,(0,255,255),2)
		        #print("w" ,len(approx),area,perimeter)
		        return(1)	            

img=cv2.imread("test_circuit_2.jpg")
img0=cv2.imread("img_main0.png")

img9=cv2.imread("img_main9.png")

img7=cv2.imread("img_main7.png")
img4=cv2.imread("img_main4.png")
img5=cv2.imread("img_main5.png")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 100, 100)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours

i=0
for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    
    if(area>700): 
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
        x, y, w, h = cv2.boundingRect(cnt)
        if(len(approx)==6):
            #cv2.rectangle(img,(x-10,y-10),(x+w+13,y+h+10),(255,255,0),1) 
            #cv2.imwrite("img_main"+str(i)+".png",img[y-10:y+h+10,x-10:x+w+13])
            i=i+1
            #img_cr = cv2.resize(img[y-10:y+h+10,x-10:x+w+13],(81,58),interpolation=cv2.INTER_CUBIC)
            #print(img[y-10:y+h+10,x-10:x+w+13].shape)
            if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(img0)):
                
                print("enter and")
                if(curve_detect(img[y-10:y+h+10,x-10:x+w+13])):
                    print("exit and")
                else:
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-img0)==0 ):
                        cv2.putText(img, "and_enter_and", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                        #print(img6)
                        #print("img in circuit")
                        #print(img[y-10:y+h+10,x-10:x+w+13])
                        if(detect_circle(img[y-10:y+h+10,x-10:x+w+13])):
                    	    cv2.putText(img, "NAND", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                        else:
                            cv2.putText(img, "AND", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
            if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(img9)):
                print("enter or")
                if(np.all(img[y-10:y+h+10,x-10:x+w+13]-img9)==0 ):
                    cv2.putText(img, "or_enter", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                	
                    #print(img6)
                    #print(img[y-10:y+h+10,x-10:x+w+13])
                    if(detect_circle(img[y-10:y+h+10,x-10:x+w+15])):
                    	if(curve_detect(img[y-10:y+h+10,x-10:x+w+15])):
                    	    cv2.putText(img, "XNOR", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                    	else:  
                    	    cv2.putText(img, "NOR", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)  
                    else:
                    	if(curve_detect(img[y-10:y+h+10,x-10:x+w+15])):
                    	    cv2.putText(img, "XOR", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                    	else:  
                    	    cv2.putText(img, "OR", (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
                        	    
                	       
            
 
cv2.imshow("1",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()  
