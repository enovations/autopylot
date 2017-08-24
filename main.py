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
from controller_navigation import Navigation
from filter import Filter

if __conf__.run_flask:
    try:
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
omega_filter = Filter([1, 2, 4], 3)
navigation = Navigation()
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


def input_handler():
    # while True:
    #     # navigation.current_dest = input('dest: ')
    #     # print(navigation.current_dest)
    #     a = 1
    pass


if not nopi:
    new_image_thread = threading.Thread(target=new_image).start()
    threading.Thread(target=input_handler()).start()

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
        dark = avg_bright < 65
        if dark:
            image = cv2.bitwise_not(image)

        image = image_process.transform_image(image)
        image = image_process.crop_and_resize_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        image = image_process.threshold_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        matches = line_detection.detect(image, masks)

        if len(matches) > 0:
            if __conf__.run_flask:
                imgs.append(image)
                if len(matches) == 1:
                    imgs.append(matches[0][-1])
                else:
                    imgs.append(cv2.bitwise_or(matches[0][-1], matches[1][-1]))

            # decide where to go
            if navigation.current_dest == None:
                ros_control.update_robot(0, 0)
            else:
                if len(matches) == 1:  # follow the only line
                    r = float(matches[0][0]) * __conf__.meter_to_pixel_ratio
                    p = matches[0][2]
                    print('default', matches[0][1])
                elif navigation.get_split_direction('') == 1:  # go right
                    r = max([float(matches[0][0]),
                             float(matches[1][0])]) * __conf__.meter_to_pixel_ratio  # convert to meters
                    r *= 0.5
                    p = max([float(matches[0][2]),
                             float(matches[1][2])]) * __conf__.meter_to_pixel_ratio  # convert to meters
                    print(1, r)
                else:  # go left
                    r = min([float(matches[0][0]),
                             float(matches[1][0])]) * __conf__.meter_to_pixel_ratio  # convert to meters
                    r *= 0.5
                    p = min([float(matches[0][2]),
                             float(matches[1][2])]) * __conf__.meter_to_pixel_ratio  # convert to meters
                    print(0, r)

                v = controller_driving.get_speed(r)

                w = Filter.r_to_w(r, v)
                p *= __conf__.position_gain

                ros_control.update_robot(v, w + p * __conf__.position_gain)
        else:
            ros_control.update_robot(0.1, 0)
            if __conf__.run_flask:
                imgs.append(np.zeros((60, 160), dtype=np.uint8))
                imgs.append(np.zeros((60, 160), dtype=np.uint8))

        if __conf__.run_flask:
            image = image_process.generate_preview(imgs, [element[2] for element in matches], dark)
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
    process_image()


@atexit.register
def stop():
    ros_control.close()
    if not nopi:
        stream.close()
        rawcapture.close()
        camera.close()
