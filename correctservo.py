import socket, traceback
import serial
import os
from time import sleep

import RPi.GPIO as GPIO
import time

import sys
import serial
from mail import sendEmail
from flask import Flask, render_template, Response
#from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading
'''ser = serial.Serial('/dev/ttyUSB0',9600)
#while True:
read_serial=ser.read()
s= read_serial.decode('utf-8')
	#print (s)
print (s)
check_for_object()'''

#ser=serial.Serial('/dev/ttyUSB0',9600)
#s='1'.encode('utf-8','strict')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

p=GPIO.PWM(11,50)   #up,down
p1=GPIO.PWM(7,50)  #left,right
p.start(11)
p1.start(9.9)
#video_camera = VideoCamera(flip=True)

# App Globals (do not edit)
#app = Flask(__name__)
#app.config['BASIC_AUTH_USERNAME'] = 'team'
#app.config['BASIC_AUTH_PASSWORD'] = 'dc'
#app.config['BASIC_AUTH_FORCE'] = True
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('192.168.43.65', 5555))

        print ("Listening for broadcasts...")
        time.sleep(0.2)               
        message, address = s.recvfrom(8192)
        a =message.decode("utf-8")
        no1,no2,x1,y1,z1,no3,x2,y2,z2= a.split(",")
        print(z1)
        print(z2)#whole message signal
        a1=float(z1)
        b1=float(z2)
        s.close();
        

        if(a1>6):       #uppper limit
            a=12.3
            
        elif(a1>5):
            a=11.9
            
        elif(a1>4):
            a=11.2
            
        elif(a1>3):
            a=10.8
        elif(a1>2):
            a=10.5
            
        elif(a1>1):
            a=10.2
            
        elif(a1>0):
            a=9      #middle limit
            
        elif(a1>-1):
            a=8
            
        elif(a1>-2):
            a=7
            
        elif(a1>-3):
            a=7.5

            
        
        else:
            a=6.9
            time.sleep(0.2)  

        if(b1>13):
            #b=180#12.5
            b=2.5
        elif(b1>10):
            #b=170#12.3
            b=3.2
        elif(b1>8):
            #b=160#11.7
            b=3.9
        elif(b1>7):
            #b=150#11.1
            b=4.6
        elif(b1>5):
            #b=140#10.5
            b=5.3
        elif(b1>4):
             #b=130#9.9
            b=6.0
        elif(b1>3):
            #b=120#9.3
            b=6.7
        elif(b1>2):
            #b=110#8.7
            b=7.3
        elif(b1>1):
                #b=100#8.1
            b=7.5
        elif(b1>0):
            #b=90 #7.5
            b=8.1 
        elif(b1>-5):
            #b=80#7.3
            b=8.5
        elif(b1>-7):
            #b=60#6.7
            b=8.9
        elif(b1>-9):
            #b=50#6.0
            b=9.0
        elif(b1>-15):
            #b=40#5.3
            b=10.5
        elif(b1>-17):
            #b=30#4.6
            b=11.1
        elif(b1>-20):
            #b=20#3.9
            b=11.7
        elif(b1>-21):
            #b=10#3.2
            b=12.3
        else:
            #b=0#2.5
            b=12.5

        p1.ChangeDutyCycle(b)
        time.sleep(0.4)
        p.ChangeDutyCycle(a)
        time.sleep(0.4)               #ser.write(s)
    except(KeyboardInterrupt, SystemExit):
        raise
        
'''@app.route('/')
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
    app.run(host='192.168.43.65', debug=False)'''
