import cv2
import numpy as np

import __conf__
from control import controller_traffic

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


def generate_preview(images, positions, dark, path, v):
    img = np.vstack(images)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    cv2.line(img, (80, 120), (80, 180 + 60), (255, 0, 255), 1)

    for position in positions:
        cv2.line(img, (80 + position, 120), (80 + position, 180 + 60), (100, 255, 255), 1)

    for i in range(2, len(images) + 2):
        if not i == 3:
            cv2.line(img, (0, 60 * i), (160, 60 * i), (255, 255, 255), 1)

    cv2.putText(img, 'transformed', (1, 130), cv2.FONT_HERSHEY_PLAIN, 0.7, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold', (1, 60 + 190), cv2.FONT_HERSHEY_PLAIN, 0.7, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(img, 'threshold & match', (1, 60 + 250), cv2.FONT_HERSHEY_PLAIN, 0.7, (180, 180, 180), 1, cv2.LINE_AA)
    cv2.putText(img, 'best curve match', (1, 60 + 310), cv2.FONT_HERSHEY_PLAIN, 0.7, (180, 180, 180), 1, cv2.LINE_AA)

    limit = v * 3.6
    cv2.putText(img, 'v: ' + ('{0:.2f}'.format(limit)) + ' km/h', (5, 13), cv2.FONT_HERSHEY_PLAIN, 0.8,
                (255, 255, 0), 1, cv2.LINE_AA)
    print(path)
    cv2.putText(img, 'p: ' + ' > '.join(path), (5, 26), cv2.FONT_HERSHEY_PLAIN, 0.8,
                (100, 255, 0), 1, cv2.LINE_AA)
    if dark:
        cv2.putText(img, 'DARK', (123, 13), cv2.FONT_HERSHEY_PLAIN, 0.8,
                    (0, 0, 255), 1, cv2.LINE_AA)

    return img


def get_masks(resolution=(160, 60)):
    brush_size = int(4 / 160 * resolution[0])
    min_rad = int(resolution[0] * 0.16) * 2
    max_rad = int(resolution[0] * 3.5)

    center = (
        resolution[0] // 2,
        resolution[1] + (2 * __conf__.pixel_25cm_distance - __conf__.first_cut_to_image_edge_in_pixels))

    masks = {}
    step = 2
    offset_step = 160 // __conf__.num_of_mask_offsets
    r = min_rad
    while r <= max_rad:
        # create left arc
        left = []
        for i in range(__conf__.num_of_mask_offsets):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (i * offset_step - r, center[1]), r, 255, brush_size)
            left.append(img)

        # create right arc
        rigth = []
        for i in range(__conf__.num_of_mask_offsets):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (i * offset_step + r, center[1]), r, 255, brush_size)
            rigth.append(img)

        masks[-r] = left
        masks[r] = rigth

        r += step
        step = int(step * 1.5)

    # create straight line
    straight = []
    for i in range(__conf__.num_of_mask_offsets):
        img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
        cv2.line(img, (i * offset_step, 0), (i * offset_step, resolution[1]), 255, brush_size)
        straight.append(img)
    masks[0] = straight
    return masks
