
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

cap = cv2.VideoCapture(f'http://127.0.0.1/stream0?streamkey={os.getenv("STREAM_KEY")}')

while True:
    ret, img = cap.read()

    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # performing binary thresholding
    kernel_size = 3
    ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)  

    # finding contours 
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # drawing Contours
    radius =2
    color = (30,255,50)
    cv2.drawContours(img, cnts, -1,color , radius)
    cv2.imshow('Video', img)

    if cv2.waitKey(1) == 27:  # escape key
        exit(0)