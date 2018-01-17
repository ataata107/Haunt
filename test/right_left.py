# KeyLogger_tk2.py
# show a character key when pressed without using Enter key
# hide the Tkinter GUI window, only console shows

try:
    # Python2
    import Tkinter as tk
    import numpy as np
    import cv2
    import serial
    global val
except ImportError:
    # Python3
    import tkinter as tk
def key(event):
    """shows key or tk code for the key"""
    
    global val
    global oldval
    ret, img = cap.read()
    if event.keysym == 'Escape':
        root.destroy()
    if event.keysym == 'Right':
        val= oldval-0.5
    elif event.keysym == 'Left':
        val=oldval+0.5
    oldval = val
    if(val>180 or val<0):
        val=90
    #ser.write("%s\n"%val)
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    
    print val
    
#ser = serial.Serial('COM10',9600)
oldval = 90
cap = cv2.VideoCapture(0)

root = tk.Tk()
print( "Press a key (Escape key to exit):" )
root.bind_all('<Key>', key)
# don't show the tk window
root.withdraw()

root.mainloop()
