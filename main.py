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
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'team'
app.config['BASIC_AUTH_PASSWORD'] = 'dc'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0



              

def check_for_objects():
    global last_epoch
    while True:
        try:
            
            frame, found_obj = video_camera.get_object(object_classifier)
            if found_obj:
                print("Human")
                print("calling")
                #bl=True
                ser.write(s)
                
            frame1, found_obj1 = video_camera.get_object(full)
            if found_obj1:
                print ("human")
                    #sendEmail(frame)
                print ("calling")
                #bl=True
                ser.write(s)
                
            frame2, found_obj2 = video_camera.get_object(up)
            if found_obj2:
                print ("human")
                    #sendEmail(frame)
                print ("done!")
                ser.write(s)
                
        except:
            print ("Error calling: ", sys.exc_info()[0])

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='192.168.43.65', debug=False)
    
