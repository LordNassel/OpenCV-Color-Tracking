#Color Filtering Programcode - only for one specific color

import cv2
import numpy as np

cap = cv2.VideoCapture(0) # 0 for webcam, 1 for other cam in logical order

                      
#Frame:
while True:
    _, frame = cap.read()
    #hsv: Hue Saturation Value, cvt: convert COLOR...
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    # hsv = hue sat value
    lower_red = np.array([150,150,50])
    upper_red = np.array([180,255,150])
    
    
    #GREEN WITH RED NAMES!
    #lower_red = np.array([45,100,50])
    #upper_red = np.array([90,255,255])
   
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask = mask)  #res=Result
    
    cv2.imshow('frame', frame) #To show!
    cv2.imshow('mask', mask) #To show! 
    cv2.imshow('res', res) #To show! 
    
    k=cv2.waitKey(5) & 0XFF #EXIT
    if k==27:
        break
    
cv2.destroyAllWindows()
cap.release() #let my webcam go! :D

    
