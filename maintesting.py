import cv2
import sys
import serial
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
import os
#import correctservo.py

video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier
full = cv2.CascadeClassifier("models/fullbody_recognition_model.xml")
up = cv2.CascadeClassifier("models/upperbody_recognition_model.xml")
ser=serial.Serial('/dev/ttyUSB0',9600)
s='1'.encode('utf-8','strict')
#s='2'.encode('utf-8','strict')
#count=0
#bl=False
# sends an email only once in this time interval
'''readSerial=ser.read()
ss=readSerial.decode('utf-8')
print(ss)'''

# App Globals (do not edit)
while True:
    try:
            
        frame, found_obj = video_camera.get_object(object_classifier)
        if found_obj:
            print("Human")
            print("calling")
                #bl=True
            ser.write(s)
            #delay(3000)
            os.system('python3 correctservo.py')
                
        frame1, found_obj1 = video_camera.get_object(full)
        if found_obj1:
            print ("human")
                    #sendEmail(frame)
            print ("calling")
                #bl=True
            ser.write(s)
            delay(3000)
            os.system('python3 correctservo.py')
                
        frame2, found_obj2 = video_camera.get_object(up)
        if found_obj2:
            print ("human")
                    #sendEmail(frame)
            print ("done!")
            ser.write(s)
            #delay(3000)
            os.system('python3 correctservo.py')
                
    except:
        print ("Error calling: ", sys.exc_info()[0])


