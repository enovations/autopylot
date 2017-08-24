import cv2
import numpy as np
import controller_traffic

import __conf__

mask = None


def init():
    # create crop mask with our transformation
    global mask
    mask = np.zeros((480, 640), dtype=np.uint8)
    mask[:] = 255
    mask = transform_image(mask)
    cv2.erode(mask, None, dst=mask, iterations=2)
    mask = crop_and_resize_image(mask)


def transform_image(img):
    matrix = cv2.getPerspectiveTransform(__conf__.pts1, __conf__.pts2)
    img = cv2.warpPerspective(img, matrix, __conf__.full_dim)
    return img


def crop_and_resize_image(image):
    img = cv2.resize(image, __conf__.proc_dim)
    return img[60:120, 0:160]


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def threshold_image(image):
    global mask
    img = cv2.medianBlur(image, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 4)

    img = cv2.bitwise_and(img, mask)

    return img


def generate_preview(images, positions, dark):
    img = np.vstack(images)

    cv2.line(img, (80, 120), (80, 180+60), (255, 0, 255), 1)

    for position in positions:
        cv2.line(img, (80 + position, 120), (80 + position, 180+60), (100, 255, 255), 1)

    for i in range(2, len(images) + 2):
        if not i == 3:
            cv2.line(img, (0, 60 * i), (160, 60 * i), (255, 255, 255), 1)

    cv2.putText(img, 'transformed', (1, 130), cv2.FONT_HERSHEY_PLAIN, 0.7, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold', (1, 60+190), cv2.FONT_HERSHEY_PLAIN, 0.7, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold & match', (1, 60+250), cv2.FONT_HERSHEY_PLAIN, 0.7, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(img, 'best curve match', (1, 60+310), cv2.FONT_HERSHEY_PLAIN, 0.7, (100, 100, 100), 1, cv2.LINE_AA)

    limit = controller_traffic.speed_limit * 3.6
    cv2.putText(img, 'Limit: ' + ('{0:.1f}'.format(limit)) + ' km/h', (5, 13), cv2.FONT_HERSHEY_PLAIN, 0.8,
                (255, 255, 0), 1, cv2.LINE_AA)
    if dark:
        cv2.putText(img, 'DARK', (123, 13), cv2.FONT_HERSHEY_PLAIN, 0.8,
                    (0, 0, 255), 1, cv2.LINE_AA)

    return img
