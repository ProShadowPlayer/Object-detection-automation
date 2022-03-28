
import cv2
import RPi.GPIO as GPIO
import time
################################################################
path = '/home/nico/opencv/haarcascade/haarcascade_eye.xml'  # PATH OF THE CASCADE
cameraNo = 0  # CAMERA NUMBER
objectName = 'EYE'  # OBJECT NAME TO DISPLAY
frameWidth = 640  # DISPLAY WIDTH
frameHeight = 480  # DISPLAY HEIGHT
color = (255, 0, 255)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
#################################################################
cap = cv2.VideoCapture(cameraNo)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
def empty(a):
    pass
# CREATE TRACKBAR
cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight + 100)
cv2.createTrackbar("Scale", "Result", 400, 1000, empty)
cv2.createTrackbar("Neig", "Result", 8, 50, empty)
cv2.createTrackbar("Min Area", "Result", 0, 100000, empty)
cv2.createTrackbar("Brightness", "Result", 45, 255, empty)
# LOAD THE CLASSIFIERS DOWNLOADED
cascade = cv2.CascadeClassifier(path)
while True:
    timer = cv2.getTickCount()
    objcount = 0
    # SET CAMERA BRIGHTNESS FROM TRACKBAR VALUE
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)
    # GET CAMERA IMAGE AND CONVERT TO GRAYSCALE
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # DETECT THE OBJECT USING THE CASCADE
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result") / 1000)
    neig = cv2.getTrackbarPos("Neig", "Result")
    objects = cascade.detectMultiScale(gray, scaleVal, neig)
    # DISPLAY THE DETECTED OBJECTS
    for (x, y, w, h) in objects:
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, objectName, (x, y - 5),
cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_color = img[y:y + h, x:x + w]
            objcount = objcount + 1
    #TOP LEFT BOX
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.rectangle(img, (250, 100), (20, 20), (0, 0, 255), 2)
    cv2.putText(img,"FPS:",(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2,)
    cv2.putText(img,str(int(fps)),(110,50),cv2.FONT_HERSHEY_SIMPLEX,1,(50, 205, 50),2)
    cv2.putText(img,"ObjCOUNT:", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
    cv2.putText(img,str(int(objcount)),(200,80),cv2.FONT_HERSHEY_SIMPLEX,1,(50, 205, 50),2)
    #LED STATUS
    if objcount > 0:
        GPIO.output(2,GPIO.HIGH)

    else:
        GPIO.output(2,GPIO.LOW)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
