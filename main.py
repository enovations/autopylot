import cv2
import time
import threading

from flask import Flask, Response

import image_process

nopi = False
image = None

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except:
    nopi = True

# init camera if can
if not nopi:
    camera = PiCamera()
    camera.resolution = (640, 480)
    # camera.shutter_speed = 6000000
    # camera.exposure_mode = 'off'
    # camera.iso = 800

app = Flask(__name__)


def new_image():
    global image
    if nopi:
        image = cv2.imread('sample.jpg')
    else:
        rawcapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawcapture, format='bgr')
        image = rawcapture.array

    image = image_process.transform_image(image)

    time.sleep(0.1)


t = threading.Thread(target=new_image)
t.start()


def gen():
    global image
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', image)[1].tostring() + b'\r\n\r\n')


@app.route('/')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8063)
