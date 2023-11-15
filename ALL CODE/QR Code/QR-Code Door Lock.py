import cv2
import RPi.GPIO as GPIO
import time

relay = 21;
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(relay , GPIO.OUT)
GPIO.output(relay , 0)
GPIO.output(relay , 1)

# set up camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()

prevTime=0
doorUnlock= False

while (True):    
    # get the image
    _, img = cap.read()
    
    # get bounding box coords and data
    data, bbox, _ = detector.detectAndDecode(img)
    
    # if there is a bounding box, draw one, along with the data
    if(bbox is not None):
        
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 255), thickness=2)
            
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        
        
        
        if data:
            print("data found: ", data)
            
            if data == 'NISHANTH' or data == 'PREETISH':
                print('Access Granted')
                
                GPIO.output(21 , 0)
                prevTime = time.time()
            
                doorUnlock = True
                print('Door Open ')
                    
            else:
                print('Access Denied')
                
    
   
    if doorUnlock == True and time.time() - prevTime > 5:    
        doorUnlock = False
        GPIO.output(21 , 1)
        print('Door Locked ')            
                
       
    cv2.imshow("code detector", img)
    
    
    if(cv2.waitKey(1) == ord("q")):
        break
