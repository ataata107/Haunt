from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from math import degrees
import numpy as np
import imutils
import cv2
import serial
ser = serial.Serial('COM10',9600)
#cap = cv2.VideoCapture(0)
cap = WebcamVideoStream(src=1).start()
val=90
while 1:
    img = cap.read()
    cv2.imshow('img',img)
    
    k = cv2.waitKey(30) & 0xff
    
    
    if k == 97:
        val += 1
    elif k == 100:
        val -= 1
    
    if(val>180 or val<0):
        val=90
    
    if k == 27:
        break
    print (val)
    ser.write("%s\n"%val) 
cap.release()
cv2.destroyAllWindows() 
