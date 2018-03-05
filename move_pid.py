import numpy as np
import cv2
import serial
from web import WebcamVideoStream



import imutils
from PID import PIDController
#ser = serial.Serial('/dev/ttyACM0',9600)
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#cap = WebcamVideoStream(src=0).start()
cap = cv2.VideoCapture(0)
val=90
Center_x=0
#-----------------------------------PID------------------------------------------
pid = PIDController(proportional = 0.015, derivative_time = 0, integral_time=0)
pid.vmin, pid.vmax = -10, 10
pid.setpoint = 0.0   #aTargetDifference(m)
TDifference = pid.setpoint
baseAngle = 90

pidout = 0
i=0
while 1:
    i+=1
    center_x=[]
    center_y=[]
    ret,img = cap.read()
    img = cv2.resize(img, (120, 140))
    if i%1 ==0:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        CENTER=img.shape[0]/2
    
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            center_x.append(x)
            center_y.append(y)
        print(len(center_x))
        if(len(center_x)>0):
            a=center_x[0]
            for i in range((len(center_x))-1):
                if(abs(CENTER-center_x[i+1])<abs(CENTER-a)):
                    a=center_x[i+1]
            print(a, "Following center",CENTER)
            current_difference = (a-CENTER)
            print ("Difference left %s" % (TDifference - current_difference))
    
            pidout = pid.compute_output(current_difference)
            pidout += baseAngle
            val=pidout
            if(a > CENTER ):
                print("<<<<<<<<<")
            
            elif(a< CENTER):
                print(">>>>>>>>>")
            
        if(val>180 or val<0):
            val=90
   # ser.write("%s\n"%val)     
    print("val",val)    
    baseAngle=val
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows() 
