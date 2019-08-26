import io
import picamera
import socket, traceback
import serial
from time import sleep
import RPi.GPIO as GPIO
import time
import logging
import socketserver
import _thread
from threading import Condition
from http import server

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)

p=GPIO.PWM(7,50)
p1=GPIO.PWM(11,50)
p.start(8)
p1.start(7.5)

PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

def streaming():
    class StreamingOutput(object):
        def __init__(self):
            self.frame = None
            self.buffer = io.BytesIO()
            self.condition = Condition()

        def write(self, buf):
            if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            return self.buffer.write(buf)

    class StreamingHandler(server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                self.send_error(404)
                self.end_headers()

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        #camera.rotation = 90
        camera.start_recording(output, format='mjpeg')
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
def servo():
    
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
        print(a)
        print(no1)
        print(no2)
        print(x1)
        print(y1)
        print(z1)
        print(no3)
        print(x2)
        print(y2)
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
            b=12.5
        elif(b1>10):
            #b=170#12.3
            b=12.3
        elif(b1>8):
            #b=160#11.7
            b=11.7
        elif(b1>7):
            #b=150#11.1
            b=11.1
        elif(b1>5):
            #b=140#10.5
            b=10.5
        elif(b1>4):
             #b=130#9.9
             b=9.9
        elif(b1>3):
            #b=120#9.3
            b=9.3
        elif(b1>2):
            #b=110#8.7
            b=8.7
        elif(b1>1):
            #b=100#8.1
            b=8.1
        elif(b1>0):
            #b=90 #7.5
            b=7.5  
        elif(b1>-5):
            #b=80#7.3
            b=7.3
        elif(b1>-7):
            #b=60#6.7
            b=6.7
        elif(b1>-9):
            #b=50#6.0
            b=6.0
        elif(b1>-14):
            #b=40#5.3
            b=5.3
        elif(b1>-17):
            #b=30#4.6
            b=4.6
        elif(b1>-20):
            #b=20#3.9
            b=3.9
        elif(b1>-21):
            #b=10#3.2
            b=3.2
        else:
            #b=0#2.5
            b=2.5

        p1.ChangeDutyCycle(b)
        time.sleep(0.4)
        p.ChangeDutyCycle(a)
        time.sleep(0.4)
        
        
        
    
     

       
        
              
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
        
while True:
    try:
       _thread.start_new_thread(streaming)
       _thread.start_new_thread(servo)
    except:
       print "Error: unable to start thread"