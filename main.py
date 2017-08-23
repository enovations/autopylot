import time
import threading
import io
import numpy as np

import cv2
from flask import Flask, Response

import image_process
import line_detection
import generate_masks

nopi = False
sendimagedata = None

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    nopi = True

# init camera if can
if not nopi:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    # camera.shutter_speed = 6000000
    # camera.exposure_mode = 'off'
    # camera.iso = 800
    time.sleep(2)
    camera.start_preview()

app = Flask(__name__)

masks = generate_masks.get_masks()

def new_image():
    global sendimagedata

    while True:

        if nopi:
            image = cv2.imread('sample.jpg')
        else:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                image = stream.array

        image = image_process.transform_image(image)
        image = image_process.crop_and_resize_image(image)
        image = image_process.threshold_image(image)
        r, image = line_detection.get_radius(image, masks)
        print(r)

        sendimagedata = cv2.imencode('.jpg', image)[1].tostring()

t = threading.Thread(target=new_image)
t.start()


def gen():
    global sendimagedata
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + sendimagedata + b'\r\n\r\n')


@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
