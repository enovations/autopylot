import cv2
import time
import threading

from flask import Flask, Response

import image_process
import line_detection

nopi = False
sendimagedata = None

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
    global sendimagedata
    if nopi:
        image = cv2.imread('sample.jpg')
    else:
        rawcapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawcapture, format='bgr')
        image = rawcapture.array

    image = image_process.threshold_image(image)
    image = image_process.transform_image(image)
    image = image_process.crop_image(image)
    image = image_process.resize(image)
    line_detection.get_omega(image)

    sendimagedata = cv2.imencode('.jpg', image)[1].tostring()

    time.sleep(0.5)


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
