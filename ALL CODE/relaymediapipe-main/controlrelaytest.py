import cv2
from vidgear.gears import PiGear
from collections import Counter
from module import findnameoflandmark,findpostion
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 

#cap = cv2.VideoCapture(0)
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]
pin1=20
pin2=21
pin3=26
GPIO.setup(pin1,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(pin3,GPIO.OUT)
options = {
#    "vflip": True,
    "exposure_mode": "auto",
    "iso": 500,
    "exposure_compensation": 10,
    "awb_mode": "horizon",
    "sensor_mode": 0,
}

# open pi video stream with defined parameters
stream = PiGear(resolution=(640, 480), framerate=80, logging=True, **options).start()

while True:

#     ret, frame = cap.read()
#     flipped = cv2.flip(frame, flipCode = -1)
#     frame1 = cv2.resize(flipped, (640, 480))
     frame = stream.read()
     frame1 = cv2.flip(frame, flipCode = 1)
    
     
     a=findpostion(frame1)
     b=findnameoflandmark(frame1)
     
      
     
     if len(b and a)!=0:
        finger=[]
        if a[0][1:] < a[4][1:]: 
           finger.append(1)
           print (b[4])
          
        else:
           finger.append(0)   

        
        
        
        fingers=[] 
        for id in range(0,4):
            if a[tip[id]][2:] < a[tip[id]-2][2:]:
               print(b[tipname[id]])
              

               fingers.append(1)
    
            else:
               fingers.append(0)
     x=fingers + finger
     c=Counter(x)
     up=c[1]
     down=c[0]
     print(up)
     print(down)
     if up == 5:
         GPIO.output(20, GPIO.HIGH)
         GPIO.output(21, GPIO.HIGH)
         GPIO.output(26, GPIO.HIGH)
    
     if down == 3:
         GPIO.output(20, GPIO.LOW)
         GPIO.output(21, GPIO.LOW)
         GPIO.output(26, GPIO.LOW)
     elif down == 1:
         GPIO.output(20, GPIO.LOW)
         GPIO.output(21, GPIO.HIGH)
         GPIO.output(26, GPIO.HIGH)
     if up == 3:
         GPIO.output(20, GPIO.HIGH)
         GPIO.output(21, GPIO.HIGH)
         GPIO.output(26, GPIO.LOW)
     elif up == 1:
         GPIO.output(20, GPIO.HIGH)
         GPIO.output(21, GPIO.LOW)
         GPIO.output(26, GPIO.LOW)  
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     if key == ord("q"):
        break
   

