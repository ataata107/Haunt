# -*- coding: utf-8 -*-
import cv2
import sys
import serial
from PID import PIDController
x=0
y=0
# import the necessary packages
from threading import Thread
import cv2
 
class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
 
	def read(self):
		# return the frame most recently read
		return self.frame
 
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

        def imshow(self):
                cv2.imshow('img',self.frame)

ser = serial.Serial('/dev/ttyACM0',9600)
pid = PIDController(proportional = 0.015, derivative_time = 0, integral_time=0)
pid.vmin, pid.vmax = -10, 10
pid.setpoint = 0.0   #aTargetDifference(m)
TDifference = pid.setpoint
baseAngle = 90
pidout = 0

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
font=cv2.FONT_HERSHEY_SIMPLEX
video_capture = WebcamVideoStream(src=0).start()
valX=90
valY=90
# video_capture = cv2.VideoCapture(0)

while True:
    # CAPTURE FRAME-BY-FRAME
    center_x=[]
    center_y=[]
    frame = video_capture.read()
    frame= cv2.resize(frame,(240,200))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    CENTERX = frame.shape[0] / 2
    CENTERY = frame.shape[1] / 2
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50),
        #when the values are smallers, the face to detect can be smaller
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE

    )
    x=y=w=h=0
    # DRAW A RECTANGLE AROUND THE FACES FOUND
    for (x, y, w, h) in faces:
        # ---To draw a rectangle this are the parameters
        # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
        # img is the image variable, it can be "frame" like in this example
        # x1,y1 ---------
        # |              |
        # |              |
        # |              |
        # -------------x2,y2
        # (255,0,0) are (R,G,B)
        # the last 2 is the thickness of the line 1 to 3 thin to gross
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 100), 1)

        #---To write the x,y on the middle of the rectangle.
        stringxy="+%s,%s"%(x,y) # To prepare the string with the xy values to be used with the cv2.putText function
        #In the case we want to put Xxvalue,Yyvalue we can use the following line removing #.
        #stringaxy="X%s,Y%s"%(x,y) 
        cv2.putText(frame,stringxy,(x+w/2,y+h/2),font, 1,(0,0,255),1)
	center_x.append(x)
        center_y.append(y)
    print(len(center_x))
    if(len(center_x) > 0):
        a = center_x[0]
        for i in range((len(center_x)) - 1):
            if(abs(CENTERX - center_x[i + 1]) < abs(CENTERX - a)):
                a = center_x[i + 1]
        print(a, "Following center", CENTERX)
        current_differenceX = (a - CENTERX)
        #       print ("Difference left %s" % (TDifference - current_difference))

        pidout = pid.compute_output(current_differenceX)
        pidout += baseAngle
        valX = pidout
        ser.write("%s\n"%valX)
        if(a > CENTERX):
            print("<<<<<<<<<")

        elif(a < CENTERX):
            print(">>>>>>>>>")

    print(len(center_y))
    if(len(center_y) > 0):
        b = center_y[0]
        for i in range((len(center_y)) - 1):
            if(abs(CENTERY - center_y[i + 1]) < abs(CENTERY - b)):
                b = center_y[i + 1]
        print(b, "Following center", CENTERY)
        current_differenceY = (b - CENTERY)
        # print ("Difference left %s" % (TDifference - current_difference))

        # pidout = pid.compute_output(current_difference)
        # pidout += baseAngle
        # val = pidout
        if(b > CENTERY):
            print("Down")

        elif(b < CENTERY):
            print("Up")

    if(valX > 180 or valX < 0):
        valX = 90
    print("valX", valX)
    baseAngle = valX


    # DISPLAY THE RESULTING FRAME
    print(frame.shape)
    cv2.imshow('Video', frame)
    print x,y,
    print"\n"
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(faces,'x,y',(x,y),font, 2,(255,255,255),1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.stop()
cv2.destroyAllWindows()
 
