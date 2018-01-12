import numpy as np
import cv2
import serial
ser = serial.Serial('COM10',9600)
# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('C:\\Users\\ataata107\\Downloads\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
val=90
Center_x=0
while 1:
    center_x=[]
    center_y=[]
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    CENTER=img.shape[0]/2
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
        center_x.append((x+w)/2)
        center_y.append((y+h)/2)
    print(len(center_x))
    if(len(center_x)>0):
        a=center_x[0]
        for i in range((len(center_x))-1):
            if(abs(CENTER-center_x[i+1])<abs(CENTER-a)):
                a=center_x[i+1]
        print(a, "Following center",CENTER)

        if(a > CENTER ):
            print("<<<<<<<<<")
            val-=1
        elif(a< CENTER):
            print(">>>>>>>>>")
            val+=1
    if(val>180 or val<0):
        val=90
    
    ser.write("%s\n"%val)    
    print("val",val)    
    
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows() 

