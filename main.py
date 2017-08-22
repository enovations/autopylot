# import the necessary packages
nopi = False

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    nopi = True

import cv2
import time

import image_process

# init camera
camera = PiCamera()
camera.resolution = (640, 480)
#camera.shutter_speed = 6000000
#camera.exposure_mode = 'off'
#camera.iso = 800

while True:
    if nopi:
        image = cv2.imread('sample.jpg')
    else:
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format='bgr')
        image = rawCapture.array
    image_process.transform_image(image)
    time.sleep(0.1)
