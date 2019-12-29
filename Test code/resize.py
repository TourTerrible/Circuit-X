import cv2
import numpy as np
img=cv2.imread("img_main9.png")
tx=53
ty=73


print(np.shape(img))

ix=np.shape(img)[0]
iy=np.shape(img)[1]

img_new=[]


#b=np.vstack((img[51],x))
#print(np.shape(b))

cx=tx-ix
cy=ty-iy

if(cy==1 and cx==0):
    img_new=np.ones((tx,ty,3),dtype=int)
    for i in range(0,ix):
        img_new[i]=np.concatenate((img[i],[img[i][iy-1]]),axis=0)
'''if(cy==2):
    img_new=np.ones((tx,ty,3),dtype=int)
    for i in range(0,ix):
        img_new[i]=np.concatenate((img[i],[img[i][iy-1]],[img[i][iy-1]]),axis=0)
if(cy==3):
    img_new=np.ones((tx,ty,3),dtype=int)
    for i in range(0,ix):
        img_new[i]=np.concatenate((img[i],[img[i][iy-1]],[img[i][iy-1]],[img[i][iy-1]]),axis=0)        
'''
if(cx==1 and cy==0):
    img_new=np.ones((tx,ty,3),dtype=int)
    for i in range(0,ix):
        img_new[i]=img[i]
    img_new[ix]=img[ix-1]   

if(cx==1 and cy==1):
    img_new=np.ones((tx,ty-1,3),dtype=int)
    img_new_2=np.ones((tx,ty,3),dtype=int)
    for i in range(0,ix):
        img_new[i]=img[i]
    img_new[ix]=img[ix-1]
    for i in range(0,ix):
        img_new_2[i]=np.concatenate((img_new[i],[img_new[i][iy-1]]),axis=0)
    print(np.shape(img_new_2))




    #img_new[i]=np.append(img[i],[img[i][iy-1]],axis=0)




cv2.waitKey(0)
cv2.destroyAllWindows() 