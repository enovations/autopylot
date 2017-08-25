import atexit
import socket
import threading
import time

import cv2
import numpy as np

import __conf__
import controller_driving
import controller_lights
import controller_navigation
import controller_ros
import controller_traffic
import detector_aruco
import detector_line
import detector_trafficsign
import image_process
from controller_navigation import Navigation
from filter import Filter

if __conf__.run_flask:
    try:
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
omega_filter = Filter([1, 2, 3, 4], 3)
navigation = Navigation()
piimage = None


def check_tethered_mode():
    try:
        import urllib.request
        urllib.request.urlopen("http://google.com").read()
        print('network reachable, going into tethered mode (won\'t move)')
        __conf__.max_speed = 0
        __conf__.max_w = 0
    except:
        pass


nounix = False

try:
    socket.AF_UNIX
except:
    nounix = True
    print('This OS does not have Unix sockets!')

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

    check_tethered_mode()


def new_image():
    global piimage
    for f in stream:
        piimage = f.array
        rawcapture.truncate(0)


def input_handler():
    server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server.bind('/tmp/autopylot_input_socket')
    while True:
        datagram = server.recv(1024)

        if not datagram:
            break

        dest = datagram.decode('utf8')
        controller_navigation.current_dest = dest
        print('dest set:', dest)
        time.sleep(0.05)


if not nopi:
    new_image_thread = threading.Thread(target=new_image).start()

if not nounix:
    threading.Thread(target=input_handler).start()

# init image_process
image_process.init()

# generate turn masks
masks = image_process.get_masks()

# init ros_control
controller_ros.init()

# init sign templates
detector_trafficsign.load_templates()

# init zmigovce
controller_lights.init()


def process_image():
    global sendimagedata, piimage

    while True:
        if nopi:
            image = cv2.imread('sample.jpg')
        else:
            image = piimage

        # grayscale image
        image = image_process.grayscale(image)

        if __conf__.run_flask:
            imgs = [cv2.resize(image, __conf__.proc_dim)]

        # find markers
        markers = detector_aruco.detect_marker(image)
        if len(markers) > 0:
            print(markers)

        # transform image
        image = image_process.transform_image(image)

        # find signs
        ###########################################
        gray = cv2.bilateralFilter(image, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = np.float32(box)

        matrix = cv2.getPerspectiveTransform(box, np.float32([[0, 0], [0, 64], [64, 64], [64, 0]]))
        detector_trafficsign.process_sign(cv2.warpPerspective(image, matrix, (64, 64)))
        ##########################################

        # check for average color, invert if white line
        avg_bright = np.average(image)
        dark = avg_bright < 65
        if dark:
            image = cv2.bitwise_not(image)

        if __conf__.run_flask:
            imgs.append(cv2.resize(image, __conf__.proc_dim))

        # crop and resize for line detection
        image = image_process.crop_and_resize_image(image)
        image = image_process.threshold_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        matches = detector_line.detect(image, masks)

        if len(matches) > 0:
            if __conf__.run_flask:
                imgs.append(image)
                if len(matches) == 1:
                    imgs.append(matches[0][-1])
                else:
                    imgs.append(cv2.bitwise_or(matches[0][-1], matches[1][-1]))

            # decide where to go
            if navigation.current_dest is None:
                controller_ros.update_robot(0, 0)
            else:
                if len(matches) == 1 or len(markers) == 0 or markers[0][1] is False:  # follow the only line
                    r = float(matches[0][0])
                    p = matches[0][2]
                else:  # ask for navigation
                    turn = navigation.get_split_direction(controller_traffic.aryco_id_to_split_name[markers[0][0]])

                    if turn == 1:
                        r = min([float(matches[0][0]),
                                 float(matches[1][0])])
                        p = min([float(matches[0][2]),
                                 float(matches[1][2])])
                        print('right')
                    else:  # go left
                        r = max([float(matches[0][0]),
                                 float(matches[1][0])])
                        p = max([float(matches[0][2]),
                                 float(matches[1][2])])
                        print('left')

                r *= __conf__.meter_to_pixel_ratio
                p *= __conf__.meter_to_pixel_ratio

                v = controller_driving.get_speed(r)

                if len(matches) > 1:
                    v = 0.1

                w = Filter.r_to_w(r, v)
                p *= __conf__.position_gain

                controller_ros.update_robot(v, w + p * __conf__.position_gain)
        else:
            controller_ros.update_robot(0.1, 0)
            if __conf__.run_flask:
                imgs.append(np.zeros((60, 160, 1), dtype=np.uint8))
                imgs.append(np.zeros((60, 160, 1), dtype=np.uint8))

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
    controller_ros.close()
    if not nopi:
        stream.close()
        rawcapture.close()
        camera.close()
    controller_lights.close()
