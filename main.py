
import cv2
import os
from dotenv import load_dotenv
import asyncio
import socketio
from concurrent.futures import ProcessPoolExecutor

load_dotenv()

cap = cv2.VideoCapture(f'http://127.0.0.1/stream0?streamkey={os.getenv("STREAM_KEY")}')

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')


async def camera_proccess():
    while True:
        ret, img = cap.read()

        # crop the image
        height, width, channels = img.shape
        croppedImage = img[int(height/2):height, 0:width] #this line crops

        # convert to gray
        gray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)

        # performing binary thresholding
        kernel_size = 3
        ret,thresh = cv2.threshold(gray,120,255,cv2.THRESH_BINARY)  

        # finding contours 
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        # drawing Contours
        radius =2
        color = (30,255,50)
        cv2.drawContours(croppedImage, cnts, -1,color , radius)
        cv2.imshow('Video', croppedImage)

        if cv2.waitKey(1) == 27:  # escape key
            exit(0)

async def main():
    await sio.connect('http://olliepugh.com', headers={"streamkey": os.getenv("STREAM_KEY")})
    asyncio.create_task(camera_proccess())

if __name__ == '__main__':
    asyncio.run(main())
    