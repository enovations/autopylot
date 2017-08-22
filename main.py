import cv2
import time

from flask import Flask, Response

import image_process

nopi = False

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


def rendered_image():
    if nopi:
        image = cv2.imread('sample.jpg')
    else:
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format='bgr')
        image = rawCapture.array

        image = image_process.transform_image(image)

    time.sleep(0.1)

    return image


def gen():
    while True:
        image = rendered_image()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', image)[1].tostring() + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
