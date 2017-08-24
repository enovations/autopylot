import __conf__

import time
import threading
import atexit

import cv2
import numpy as np

import image_process

if __conf__.run_flask:
    try:
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
piimage = None
preview_dim = (200, 150)

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
    new_image_thread = threading.Thread(target=new_image).start()

# init image_process
image_process.init()

templates = []


def load_templates():
    for i in range(0, 5):
        template = cv2.imread(str(i) + '.jpg')

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.adaptiveThreshold(template, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 5, 6)

        templates.append((i, template))

        for i2 in range(3):
            template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
            templates.append((i, template))


def match_image(image):
    curr_min = 1e20
    minx = -1

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 5, 6)

    for template in templates:
        result = cv2.matchTemplate(image, templ=template[1], method=cv2.TM_SQDIFF)
        if curr_min > result:
            curr_min = result
            minx = template[0]

    return minx


load_templates()


def process_signs(signs):
    for sign in signs:
        print(match_image(sign))


def process_image():
    global sendimagedata, piimage

    while True:
        if nopi:
            image = cv2.imread('sample.jpg')
        else:
            image = piimage

        if __conf__.run_flask:
            imgs = []
            orig_preview = cv2.resize(image, __conf__.proc_dim)
            orig_preview = image_process.grayscale(orig_preview)
            imgs.append(orig_preview)

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
