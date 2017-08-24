import numpy as np

import __conf__

import time
import threading
import atexit

import cv2

import image_process

if __conf__.run_flask:
    try:
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
piimage = None

try:
    import picamera, picamera.array
except:
    nopi = True

# init camera if can
if not nopi:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30

    time.sleep(0.3)

    rawcapture = picamera.array.PiRGBArray(camera)
    stream = camera.capture_continuous(rawcapture, format='bgr', use_video_port=True)


def new_image():
    global piimage
    for f in stream:
        piimage = f.array
        rawcapture.truncate(0)


if not nopi:
    new_image_thread = threading.Thread(target=new_image)
    new_image_thread.start()


def process_signs(signs):
    pass


def process_image():
    global sendimagedata, piimage

    preview_dim = (200, 150)

    while True:

        if nopi:
            image = cv2.imread('sample.jpg')
        else:
            image = piimage

        image = image_process.transform_image(image)

        if __conf__.run_flask:
            imgs = [cv2.resize(image, preview_dim)]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

        edged = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR)

        cv2.drawContours(edged, contours, -1, (255, 255, 0), 4)

        x_offset = 0

        signs = []

        for con in contours:
            rect = cv2.minAreaRect(con)
            box = cv2.boxPoints(rect)
            box = np.float32(box)

            matrix = cv2.getPerspectiveTransform(box, np.float32([[0, 0], [0, 100], [100, 100], [100, 0]]))
            img_sign = cv2.warpPerspective(image, matrix, (100, 100))

            edged[0:0 + img_sign.shape[0], x_offset:x_offset + img_sign.shape[1]] = img_sign

            signs.append(cv2.resize(img_sign, (32, 32)))

            x_offset += 100

        process_signs(signs)

        if __conf__.run_flask:
            imgs.append(cv2.resize(edged, preview_dim))

        if __conf__.run_flask:
            outimg = np.vstack(imgs)

            for i in range(1, len(imgs) + 1):
                cv2.line(outimg, (0, preview_dim[1] * i), (preview_dim[0], preview_dim[1] * i), (255, 255, 255), 1)

            sendimagedata = cv2.imencode('.jpg', outimg)[1].tostring()


if __conf__.run_flask:

    t = threading.Thread(target=process_image)
    t.start()

    app = Flask(__name__)


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
        app.run(host='0.0.0.0', port=__conf__.flask_port, threaded=__conf__.flask_threaded)

else:
    print('Running in daemon mode')
    process_image()


@atexit.register
def stop():
    if not nopi:
        stream.close()
        rawcapture.close()
        camera.close()
