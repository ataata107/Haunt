#run program as sudo
#use time.sleep(0.05) if servo not moving
import numpy as np
import cv2
#import serial
import Rpi.GPIO as GPIO
from PID import PIDController
#ser = serial.Serial('COM10',9600)
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
pwm = GPIO.PWM(11,50)
pwm.start(5)#change so that it becomes 90
#pwm.ChangeDutyCycle(5 or 7.5 or 10 or custom)
#pwm.stop()
#GPIO.cleanup()
#m=(y2-y1)/180, y-y1=m(x-0)=dutycycle
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('C:\\Users\\ataata107\\Downloads\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
val=90
Center_x=0
#-----------------------------------PID------------------------------------------
pid = PIDController(proportional = 0.015, derivative_time = 0, integral_time=0)
pid.vmin, pid.vmax = -10, 10
pid.setpoint = 0.0   #aTargetDifference(m)
TDifference = pid.setpoint
baseAngle = 90

pidout = 0
while 1:
    center_x=[]
    center_y=[]
    ret, img = cap.read()
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
    Dc = fun(val)
    pwm.ChangeDutyCycle(Dc)
    #ser.write("%s\n"%val)     
    print("val",val)    
    baseAngle=val
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
pwm.stop()
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows() 
