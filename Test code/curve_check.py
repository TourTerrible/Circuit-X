import cv2
import numpy as np

def delete_repeated(array2d):
    new=array2d.copy()
    total=np.shape(array2d)[0]
    for i in range(0,total):
        print(array2d[i])
        for j in range(i+1,total):
            out=np.array(np.subtract(array2d[i],array2d[j]))
            print("out:",out)
            if(np.all(out)<6):
                print("out_append:",out)
                if array2d[j] in new:
                    new.remove(array2d[j])    
    return(new)            



img=cv2.imread("test_circuit_2.jpg")

img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 80, 80)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
               # find countours around chips, see image: contours
measurements=[]
for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    if(perimeter>20 and perimeter<600): 
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
        x, y, w, h = cv2.boundingRect(cnt)
        coordinates=[x,y,w,h]
        if(len(approx)==6):
            measurements.append(coordinates)
            cv2.drawContours(img,cnt,-1,(0,255,255),2)
            #cv2.putText(img, str(area), (x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
            
           
	        
	           

#print(np.shape(measurements)[0])
print(delete_repeated(measurements))
cv2.imshow("dsa",img)
cv2.waitKey(0)
cv2.destroyAllWindows() 




