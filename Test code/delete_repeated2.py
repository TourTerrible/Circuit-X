import cv2
import numpy as np


img=cv2.imread("test_circuit_1.jpg")
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_gray=cv2.GaussianBlur(img_gray,(5,5),1)
filtered = cv2.fastNlMeansDenoising(img_gray, 8, 8, 7, 21)
edges = cv2.Canny(filtered, 80, 80)
_, contours_all,_= cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
coordinates=[]

for cnt in contours_all:
    perimeter = cv2.arcLength(cnt,True)
    area= cv2.contourArea(cnt)
    if(area>150 and perimeter<600): 
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
        x, y, w, h = cv2.boundingRect(cnt)
        if(len(approx)>=5):
            cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
            values=[x,y,w,h]
            coordinates.append(values)
            
            	        
print(coordinates)
            	        	
            		
final=[]
flag=0
flag2=0
for a in coordinates:
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

            	
#print(final)
'''
v=np.shape(coordinates)[0]
i=0
j=i+1
while(j<v):
	if(np.all(final[i]-final[j])<10):
		print("same",final[i]-final[j])
		final=np.delete(final,j,0)
		v=v-1
		j=j+1

            

'''

print(final)
            
#cv2.imshow("edges",edges) 
#cv2.imshow("1",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()                 