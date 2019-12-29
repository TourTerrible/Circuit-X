import cv2
import numpy as np

#red==1
lowerBound1=np.array([0,80,0])
upperBound1=np.array([10,255,255])

lowerBounddot=np.array([100,200,0])
upperBounddot=np.array([121,255,255])

#green==2
lowerBound2=np.array([33,80,40])
upperBound2=np.array([80,255,255])
#blue==3
lowerBound3=np.array([100,80,0])
upperBound3=np.array([121,255,255])
#yellow==4
lowerBound4=np.array([20,100,100])
upperBound4=np.array([30,255,255])

threshold_y = 5
threshold_x = 5
final_corner = []


BLUE=-3
GREEN=-2
RED=-1
YELLOW=-4

value_list = list()

connected_output_input = []

answer_table = []

# find index of coordinate variable x in the given list
def find_coordinate_index(final_corner, x):
    for i in range(len(final_corner)):
        if final_corner[i][0] == x[0] and final_corner[i][1] == x[1]:
            return i

# set value of input of gate from the connected output
def set_next_input_value(x, v):
    y = []
    for t in connected_output_input:
        if t[0][0] == x[0] and t[0][1] == x[1]:
            y = t[1]
            break
    if len(y) == 0:
        return
    final_corner[find_coordinate_index(final_corner, y)][3] = v

# delete redundant entries of absent colors
def delete_redundant(answer_table, linked_array):
    colors = {-1: 0, -2: 0, -3: 0}
    for row in linked_array:
        if row[2] < 0:
            colors[row[2]] = 1
        if row[3] < 0:
            colors[row[3]] = 1

    #print("DICT", colors)
    header_int = []

    for color, count in colors.items():
        if count == 0:
            for row in answer_table:
                del row[abs(color)-1]
        else:
            header_int.append(color)

    header = []
    for i in header_int:
        if i == RED:
            header.append("r")
        elif i == GREEN:
            header.append("g")
        else:
            header.append("b")

    header.append("o")
    data = []
    for row in answer_table:
        if tuple(row) not in data:
            data.append(tuple(row))

    new_array = []
    new_array.append(list(header))
    for row in data:
        new_array.append(list(row))

    return new_array

# Draw Truth Tables
def truth_table(linked_array, final_corner):
    for i in range(len(final_corner)):
        final_corner[i].append(0)
    for r in range(2):
        for g in range(2):
            for b in range(2):
                answer = 0
                for x in linked_array:
                    # NOT
                    if x[0] is 0:
                        v = 0
                        if x[1] == RED:
                            v = r
                        elif x[1] == GREEN:
                            v = g
                        elif x[1] == BLUE:
                                v = b
                        elif x[1] > 0:
                            try:
                                v = final_corner[find_coordinate_index(final_corner, [x[1],x[2]])][3]
                            except:
                                cv2.imshow("error",img)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()  
                        print("NOT", v)
                        if(x[5] != -4):
                            try:
                                final_corner[find_coordinate_index(final_corner, [x[5], x[6]])][3] = v^1
                                set_next_input_value([x[5], x[6]], v^1)
                            except:
                                cv2.imshow("error",img)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()   
                        else:
                            answer = v^1

                    else:
                        v1 = 0
                        v2 = 0
                        if x[1] == RED:
                            v1 = r
                        elif x[1] == GREEN:
                            v1 = g
                        elif x[1] == BLUE:
                            v1 = b
                        elif x[1] > 0:
                            v1 = final_corner[find_coordinate_index(final_corner, [x[1],x[2]])][3]
                        if x[3] == RED:
                            v2 = r
                        elif x[3] == GREEN:
                            v2 = g
                        elif x[3] == BLUE:
                            v2 = b
                        elif x[3] > 0:
                            v2 = final_corner[find_coordinate_index(final_corner, [x[3],x[4]])][3]

                        v = 0
                        if x[0] is 1:
                            v = v1 & v2
                        elif x[0] is 2:
                            v = v1 | v2
                        elif x[0] is 3:
                            v = (v1^v2)^1
                        elif x[0] is 4:
                            v = v1^v2
                        elif x[0] is 5:
                            v = (v1 | v2)^1
                        elif x[0] is 6:
                            v = v1 & v2
                                          

                        if(x[5] != -4):
                            final_corner[find_coordinate_index(final_corner, [x[5], x[6]])][3] = v
                            set_next_input_value([x[5], x[6]], v)
                        else:
                            answer = v
                answer_table.append([r, g, b, answer])
    final_answer_table = delete_redundant(answer_table, linked_array)
    # final_answer_table = answer_table
    print("Table:\n\n",np.array(final_answer_table))


def only_intermediate_output(linked_a):
    
    output_array=[]
    for i in linked_a:
        if(i[5]>0 and i[6]>0):
            
            output_array.append([i[5],i[6],0])
            
    return(output_array)

def is_initial_blue_dot(img):
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
        if(area>0 or perimeter>0 ):
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)   
            x, y, w, h = cv2.boundingRect(cnt)
            if(len(approx)>4):
                return(1)

        


def start_gate_coordinate(coordi):
    output_array=[]
    for i in coordi:
        counter=0
        for j in coordi:
            if(i[0]<=j[0]):
                counter=counter+1
            elif(abs(i[1]-j[1])>70):
                counter=counter+1 
            else:
                break       
        if(counter==np.shape(coordi)[0]):
            output_array.append(i)    
            
            
        
            
    return(output_array)



def Truthtableforonegate(type_gate):
    if(type_gate==0):
            print("input | output")
            print("1     |    0")
            print("0     |    1")
    else:
        print("i1,i2 | output")   
        if(type_gate==1):
            print("0  0  |    0")
            print("0  1  |    0")
            print("1  0  |    0")
            print("1  1  |    1")
        if(type_gate==2):
            print("0  0  |    0")
            print("0  1  |    1")
            print("1  0  |    1")
            print("1  1  |    1")
        if(type_gate==3):
            print("0  0  |    1")
            print("0  1  |    0")
            print("1  0  |    0")
            print("1  1  |    1")
        if(type_gate==4):
            print("0  0  |    0")
            print("0  1  |    1")
            print("1  0  |    1")
            print("1  1  |    0")
        if(type_gate==5):
            print("0  0  |    1")
            print("0  1  |    0")
            print("1  0  |    0")
            print("1  1  |    0")
        if(type_gate==6):
            print("0  0  |    1")
            print("0  1  |    1")
            print("1  0  |    1")
            print("1  1  |    0")

def onegatesolve(coordinates):
    
    if np.shape(coordinates)[0]==1:
        Truthtableforonegate(coordinates[0][4])                       


def checkProximity(a, b, dir):
    if(abs(a[dir] - b[dir]) <= threshold_y):
        return True
    return False

def mark_found(k):
    try:
        for i in range(len(final_corner)):
            if final_corner[i][0] == k[0] and final_corner[i][1] == k[1]:
                final_corner[i][2] = 1
    except:
        cv2.imshow("partial correct",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        #exit()  

def find_next_x(final_corner, k):
    mark_found(k)
    f = list()
    for i in final_corner:
        if checkProximity(k, i, 1):
            if i[2] == 0:
                if(len(f) is 0):
                    f = i
                else:
                    if f[0] > i[0]:
                        f = i
    
    mark_found(f)
    return f

def find_next_y(final_corner, k):
    mark_found(k)
    f = list()
    for i in final_corner:
        if checkProximity(k, i, 0):
            if i[2] == 0:
                if(len(f) is 0):
                    f = i
                else:
                    if(f[1] > i[1]) :
                        f = i
    mark_found(f)
    return f

def isInput(coordi):
    for i in linked_array:
        if float(i[1]) == coordi[0] and float(i[2]) == coordi[1]:
            return True
        if float(i[3]) == coordi[0] and float(i[4]) == coordi[1]:
            return True
    return False


def find_next_input(output_coordinate):
    mark_found(output_coordinate)
    next_x = find_next_x(final_corner, output_coordinate)
    while True:
        if isInput(next_x):
            return next_x
        next_y = find_next_y(final_corner, next_x)
        if isInput(next_y):
            return next_y
        next_x = find_next_x(final_corner, next_y)
    return -1

def remove_noise(final_corner):
    final_corner.sort(key = lambda x: [x[1], x[0]])
    for i in range(len(final_corner)):
        for j in range(len(final_corner)):
            if checkProximity(final_corner[j], final_corner[i], 0):
                final_corner[j][0] = final_corner[i][0]
            if checkProximity(final_corner[j], final_corner[i], 1):
                final_corner[j][1] = final_corner[i][1]
    final_corner.sort(key = lambda x: [x[1], x[0]])
    return final_corner

def solve(final_corner):
    for i in range(len(final_corner)):
        if final_corner[i][2] is 0:
            connected_output_input.append( [final_corner[i][:2],  find_next_input(final_corner[i])[:2]] )
    #print("connected output with next input", connected_output_input)
            


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
            #cv2.putText(img,"red",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
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
            #cv2.putText(img,"grren",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
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
        return(output_final_yellow)

def initial_blue_array(array_gates,array_corner):
    initial_blue_dot=[]
    for i in array_corner:
        c=0
        for j in array_gates:
            if(i[0]>j[0]):
            
                break
            else:
                c=c+1   
        if(c==np.shape(array_gates)[0]):
            initial_blue_dot.append(i)
    return(initial_blue_dot)

def gates_ip_op(gate_array,wires_corner_array):
    ip_op_valid=[];
    val=[]
    assoc=[]
    p=0
    for i in gate_array:
        flag3=0
        val=[0,0,0,0,0,0,0,0,0]
        for j in wires_corner_array:
            #ouput pin
            #val=[gate_number,ip1x,ip1y,ip2x,ip2y,opx,opy,x_gate,y_gate]
            

            val[7]=i[0]
            val[8]=i[1]

            
            if((i[0]+i[2]-j[0])>-50 and (i[0]+i[2]-j[0])<0 and i[1]+i[3]+5>j[1] and i[1]-5<j[1]):
                #cv2.circle(img, (j[0],j[1]), 5, (25,0,200), 2)
                op_x_y=[j[0],j[1]]
                ip_op_valid.append(op_x_y)
                val[0]=i[4]
                val[5]=j[0]
                val[6]=j[1]
                


            
            #input pins    
            if(i[0]-j[0]>0 and i[0]-j[0]<70 and i[1]+i[3]+5>j[1] and i[1]-5<j[1]):
                
                #cv2.circle(img, (j[0],j[1]), 5, (25,0,200), 2) 
                ip_x_y=[j[0],j[1]]
                ip_op_valid.append(ip_x_y)
                if(flag3==0):

                    val[0]=i[4]
                    val[1]=j[0]
                    val[2]=j[1]
                    flag3=1
                else:
                    val[0]=i[4]
                    val[3]=j[0]
                    val[4]=j[1]
        if(val[5]==0 and val[6]==0):
            if(return_red_green_flag(img[i[1]-15:i[1]+i[3]+15,i[0]+i[2]:i[0]+i[2]+60])[2]==1):
                val[5:7]=[YELLOW,YELLOW]
            else:
                print("couldnt detect output in linker function gates_ip_op\n")
                print("\nBroken wire\n")

                cv2.drawMarker(img,(val[7]+80,val[8]+12),(0,0,255),2)
                cv2.imshow("img",img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #exit()
                    
            #output x,y =-1,-1 the final output gate
        #if both detected inputs are blue input     
        #if(val[1]!=0 and val[2]!=0 and val[3]!=0 and val[4]!=0):100.0
            #val[1:5]=['i3_b','i3_b']
        #if one blue input detected
        if(val[1]!=0 and val[2]!=0 and val[3]==0 and val[4]==0):
            if(val[0]!=0):
                val[3:5]=[BLUE,BLUE]
                #print("here")
              
            #cv2.rectangle(img,(i[0]-45,i[1]-15),(i[0],i[1]+i[3]+15),(255,0,0),1)
                red_green_flag=return_red_green_flag(img[i[1]-15:i[1]+i[3]+15,i[0]-45:i[0]-15])
                if(red_green_flag[0]==1 and red_green_flag[1]==0):
                    val[1:3]=[RED,RED]
                elif(red_green_flag[0]==0 and red_green_flag[1]==1):
                    val[1:3]=[GREEN,GREEN]
                else:
                    #print("color",red_green_flag)
                    print("couldnt detect initial input color when one input is blue change green color range")    
            else:
                red_green_flag=return_red_green_flag(img[i[1]-15:i[1]+i[3]+15,i[0]-60:i[0]-15])
                if(red_green_flag[0]==1 and red_green_flag[1]==0):
                    val[1:3]=[RED,RED]
                elif(red_green_flag[0]==0 and red_green_flag[1]==1):
                    
                    val[1:3]=[GREEN,GREEN]
                else:
                    if(is_initial_blue_dot(img[i[1]-15:i[1]+i[3]+15,i[0]-60:i[0]-15])):
                        val[1:3]=[BLUE,BLUE]
                    #start_gate_coordinate
                    #print("not able to find input for not gate or intermediate not gate")    
                
                        
            
                          
                  

        #detect_other_input
        #if no blue input detected    
        if(val[1]==0 and val[2]==0 and val[3]==0 and val[4]==0):
            #img[i[1]:i[1]+i[3],i[0]-30:i[0]]

            #cv2.rectangle(img,(i[0]-45,i[1]-15),(i[0],i[1]+i[3]+15),(255,0,0),1)
            

            if(val[0]!=0):
                #print("here")
                red_green_flag=return_red_green_flag(img[i[1]-15:i[1]+i[3]+15,i[0]-45:i[0]-15])
                if(red_green_flag[0]==1 and red_green_flag[1]==1):
                    #print("asd")
                    val[1:3]=[RED,RED]
                    val[3:5]=[GREEN,GREEN]
            else:
                red_green_flag=return_red_green_flag(img[i[1]-15:i[1]+i[3]+15,i[0]-60:i[0]-15])
                
                if(red_green_flag[0]==1 and red_green_flag[1]==0):
                    val[1:3]=[RED,RED]
                elif(red_green_flag[0]==0 and red_green_flag[1]==1):
                    val[1:3]=[GREEN, GREEN]
                else:
                    val[1:3]=[BLUE,BLUE]        
                           


            #detect_both_input        

        assoc.append(val)

    #print(assoc)                
    return(ip_op_valid,assoc)            
    


def resize_and(img_extracted,img_saved):

    tx=np.shape(img_extracted)[0]
    ty=np.shape(img_extracted)[1]

    ix=np.shape(img_saved)[0]
    iy=np.shape(img_saved)[1]

    #print(ix,iy)

    
    cx=tx-ix
    cy=ty-iy

    if(cy==1 and cx==0):
        img_new=np.ones((tx,ty,3),dtype=int)
        for i in range(0,ix):
            img_new[i]=np.concatenate((img_saved[i],[img_saved[i][iy-1]]),axis=0)
        return(img_new)    

    if(cx==1 and cy==0):
        img_new=np.ones((tx,ty,3),dtype=int)
        for i in range(0,ix):
            img_new[i]=img_saved[i]
        img_new[ix]=img_saved[ix-1]  
        return(img_new) 

    if(cx==1 and cy==1):
        img_new=np.ones((tx,ty-1,3),dtype=int)
        img_new_2=np.ones((tx,ty,3),dtype=int)
        for i in range(0,ix):
            img_new[i]=img_saved[i]
        img_new[ix]=img_saved[ix-1]
        for i in range(0,ix):
            img_new_2[i]=np.concatenate((img_new[i],[img_new[i][iy-1]]),axis=0)

        #print(np.shape(img_new_2))
        return(img_new_2)
def resize_or(img):

    img_new=np.ones((53,68,3),dtype=int)
    for i in range(0,52):
        img_new[i]=img[i]
    img_new[52]=img[51]    

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
            #cv2.drawContours(img,cnt,-1,(0,255,255),2)
            corners = cv2.goodFeaturesToTrack(maskGRAY, 25, 0.05, 10)

            #holes=getLandmarks(corners)
            for i in corners:
                x,y=i.ravel()
                x_y=[x,y,0]

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

def delete_extra_wire_corners(coordinates_array_2d):
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
                if((abs(x[0]-a[0])>30 ) or (abs(x[1]-a[1])>15 ) ):
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
                #print(area,"pr",perimeter,"len",len(approx))
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
        if(area>20 and area <30 and perimeter<50): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            
            if(len(approx)>=6):
                #cv2.rectangle(img,(x-1,y-1),(x+w+1,y+h+1),(255,0,0),1) 
                #cv2.drawContours(img,cnt,-1,(0,255,255),2)
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
        # x, y, w, h = cv2.boundingRect(cnt)
        # cv2.putText(img, str(area),(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1)
        if(area>10 and perimeter<700): 
            #cv2.drawContours(img,cnt,-1,(0,255,255),2)
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            
            if(len(approx)>=5):
                #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
                
                #curve_detect(img[y-10:y+h+10,x-13:x+w+13])
                #dot_detect(img[y-10:y+h+10,x-13:x+w+13])
                #print(np.shape(img[y-10:y+h+10,x-10:x+w+13]))
                #print(np.shape(or_saved))
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])[1]==73):
                    and_saved_resized=resize_and(img[y-10:y+h+10,x-10:x+w+13],and_saved)
                    #print
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-and_saved_resized)==0 ):
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
                            #print(str(area))
                #img[y-10:y+h+10,x-10:x+w+13]=cv2.resize(img[y-10:y+h+10,x-10:x+w+13],(72,52),interpolation=cv2.INTER_LINEAR)
                else:

                    #print("enter_and")
                    if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(and_saved)):
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
                if(np.shape(img[y-10:y+h+10,x-10:x+w+13])[0]==53 and np.shape(img[y-10:y+h+10,x-10:x+w+13])[1]==68):
                    or_saved_resized=resize_or(or_saved)                
                
                    #print("enter_or")
                    if(np.all(img[y-10:y+h+10,x-10:x+w+13]-or_saved_resized)==0 ):
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
                else:
                    if(np.shape(img[y-10:y+h+10,x-10:x+w+13])==np.shape(or_saved)):
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
                                
        if(perimeter>80 and perimeter<200 and area>10 and area <600): 
            approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)           
            x, y, w, h = cv2.boundingRect(cnt)
            #cv2.drawContours(img,cnt,-1,(0,255,255),2)
            #print(area,"pr",perimeter,"len",len(approx))
            if(len(approx)>=2 and len(approx)<=6):
                t=0
                values=[x,y,w,h,t]
                coordinates.append(values)
                #cv2.drawContours(img,cnt,-1,(0,255,255),2)
                #cv2.rectangle(img,(x-15,y-10),(x+w+13,y+h+10),(255,255,0),1)
                #print(area,"pr",perimeter,"len",len(approx))
                cv2.putText(img, "NOT",(x, y), cv2.FONT_HERSHEY_COMPLEX,.4, (0, 0, 0), 1) 
                
                
                


img=cv2.imread(".jpg")
or_saved=cv2.imread("img_main0.png")
and_saved=cv2.imread("img_main9.png")
#print(find_input(img))  


coordinates=[]
identify_gates(img)

final_corner=delete_extra_wire_corners(find_wires_corner(img))
'''final_corner =[x,y] containing all wires corners which are
seperated by a threshold value as in given functio '''
final_corner.sort(key = lambda x: [x[0], x[1]])
final_corner = remove_noise(final_corner)
  
#print(" \n", np.array(final_corner))

#print(np.array(final_corner))
#for i in final_corner:
#cv2.circle(img, (i[0],i[1]), 5, (25,0,200), 2)
ip_op_array,linked_array=gates_ip_op(delete_repeated(coordinates),final_corner)

linked_array.sort(key = lambda x: [x[7], x[8]])
    
#print(np.array(linked_array))
#print(np.array(ip_op_array))
#print(np.array(delete_repeated(coordinates)))
for i in ip_op_array:
    cv2.circle(img, (i[0],i[1]), 5, (25,0,200), 2)  




#print(np.shape(ip_op_array))

'''initial_blue=initial_blue_array(delete_repeated(coordinates),ip_op_array) 
for x in initial_blue:  
    ip_op_array=np.delete(ip_op_array,np.where(ip_op_array==x),0)
print(np.shape(ip_op_array))'''


#print(delete_repeated(coordinates))
print("number of gates:", np.shape(delete_repeated(coordinates))[0])


print(count_gate_n_type(delete_repeated(coordinates)))
print("[NOT,AND,OR,XNOR,XOR,NOR,NAND]")
#print(only_intermediate_output(linked_array))

only_intermediate_output(linked_array).sort(key = lambda x: [x[0],x[1]])
if(np.shape(delete_repeated(coordinates))[0]==1):
    print("Table:")
    onegatesolve(delete_repeated(coordinates))
else:
    print("")
    solve(only_intermediate_output(linked_array))
    truth_table(linked_array,final_corner)



#print("start_gate_coordinate:",start_gate_coordinate(delete_repeated(coordinates)))



# cv2.imshow("edges",edges) 
cv2.imshow("correct",img)
#cv2.imshow("edges",edges)    
cv2.waitKey(0)
cv2.destroyAllWindows()                 