import __conf__

import time
import threading
import atexit

import cv2
import numpy as np

import image_process
import line_detection
import generate_masks
import ros_control
import controller_driving
from filter import Filter

if __conf__.run_flask:
    try:
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
omega_filter = Filter([1, 2, 3, 4], 3)
speed_filter = Filter([1, 2, 3, 4], 1)
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

# generate turn masks
masks = generate_masks.get_masks()

# init image_process
image_process.init()

# init ros_control
ros_control.init()


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

        image = image_process.grayscale(image)

        # check for color of result
        avg_bright = np.average(image)
        if avg_bright < 65:
            image = cv2.bitwise_not(image)

        image = image_process.transform_image(image)
        image = image_process.crop_and_resize_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        image = image_process.threshold_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        if __conf__.run_flask:
            r, s, position, image, mask = line_detection.get_radius(image, masks)
            imgs.append(image)
            imgs.append(mask)
        else:
            r, s, position = line_detection.get_radius(image, masks)

        v = controller_driving.get_speed(r*__conf__.meter_to_pixel_ratio, speed_filter)
        #v = v[0]

        w, _, p = omega_filter.get([Filter.r_to_w(r), s, position])
        p *= __conf__.position_gain

        ros_control.update_robot(v, w + p * __conf__.position_gain)

        if __conf__.run_flask:
            image = image_process.generate_preview(imgs, position)
            sendimagedata = cv2.imencode('.jpg', image)[1].tostring()


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
    while True:
        process_image()


@atexit.register
def stop():
    ros_control.close()
    if not nopi:
        stream.close()
        rawcapture.close()
        camera.close()
