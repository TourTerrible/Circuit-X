# Circuit-X
__With the help of Computer Vision,Generating the truth table of given digital circuit designed on Multisim.__

## Image Processing ##
*Detection of logic gates*

* We used opencv in python to detect gate.
* We detect edges with cv2.canny(...) , then perform contour detection with cv2.findContours() on that edge detected image.
* After detecting contour we applied image segmentation on contours to detect gates.
* It is given that dimensions of gates are same in every image, so we  cropped  detected gate and compared with previously saved gate .

## Gate Identification ##
*Identification of logic gates*

__Problem faced__: 
* xor,xnor and nor were detecting as OR and Nand was detecting as AND.
* sometimes shape of cropped region was bit changed, due to that we were unable to compare them.

__Solution__:
* We defined two function dot_detection and curve_detection for xor to solve problem 1.
* We defined function to resize images whenever cropped region have different shape to solve problem 2.

## Wires and their edges detection ##
 
* Simply used color of wires to detect them with the help of mask.
* To detect edges , we used cv2.goodFeaturesToTrack(...) function to detect all the corner in masked image having only blue coloured image.
* We detected all the corners of wires , and used gates coordinates stored by other function to store only gates input and output edges.
* We stored all the corners and input output corners in a 2d numpy array.  

## Linking output to next gate input ## 

* We already detected corners of  wires , so we defined a function which return next edge of wire with the help of corners of wires.
* We have already stored gate nature, coordinates, linked input and output.
* So finally we have  a set of data having next input to corresponding output, another set of data for  gate type and its input output coordinates.

## Truth-Table Generation ##


* So finally we have  a set of data having next input to corresponding output, another set of data for  gate type and its input output coordinates.
* We linked both these sets and defined a function for 3 inputs i.e max inputs, to store output values corresponding to these inputs
* For applying gate operation python already has bitwise operations.


