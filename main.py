import __conf__

import time
import atexit

import cv2

import image_process
import line_detection
import generate_masks
import ros_control
from filter import Filter

if __conf__.run_flask:
    try:
        import threading
        from flask import Flask, Response
    except:
        __conf__.run_flask = False

nopi = False
sendimagedata = None
filterus = Filter()

try:
    import picamera, picamera.array
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

# generate turn masks
masks = generate_masks.get_masks()

# init image_process
image_process.init()

# init ros_control
ros_control.init()


def new_image():
    global sendimagedata

    while True:

        if nopi:
            image = cv2.imread('sample.jpg')
        else:
            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                image = stream.array

        if __conf__.run_flask:
            imgs = []

        image = image_process.transform_image(image)
        image = image_process.crop_and_resize_image(image)
        image = image_process.grayscale(image)

        if __conf__.run_flask:
            imgs.append(image)
            imgs.append(image_process.mask)

        image = image_process.threshold_image(image)

        if __conf__.run_flask:
            imgs.append(image)

        if __conf__.run_flask:
            r, s, image, mask = line_detection.get_radius(image, masks)
            imgs.append(mask)
            imgs.append(image)
        else:
            r, s = line_detection.get_radius(image, masks)

        w = filterus.get(r, s)

        print(w, r, s)
        ros_control.update_robot(__conf__.v, w)

        if __conf__.run_flask:
            image = image_process.stitch_images(imgs)
            sendimagedata = cv2.imencode('.jpg', image)[1].tostring()


if __conf__.run_flask:

    t = threading.Thread(target=new_image)
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
    while True:
        print('Running in daemon mode')
        new_image()


@atexit.register
def stop():
    print('papa. grem pancat.')
    ros_control.update_robot(0, 0)
    picamera.close()
