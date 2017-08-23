import numpy as np
import cv2


def get_masks(resolution=(160, 40)):
    brush_size = int(4 / 160 * resolution[0])
    min_rad = int(resolution[0] * 0.16) * 2
    max_rad = int(resolution[0] * 5.31)

    center = (resolution[0] // 2, resolution[1])

    masks = {}
    step = 2
    r = min_rad
    while r <= max_rad:
        # create left arc
        left = []
        for i in range(80):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (i*2 - r, center[1]), r, 255, brush_size)
            left.append(img)

        # create right arc
        rigth = []
        for i in range(80):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (center[0] + r, center[1]), r, 255, brush_size)
            rigth.append(img)

        masks[-r] = left
        masks[r] = rigth

        r += step
        step = int(step * 1.5)

    # create straight line
    straight = []
    for i in range(80):
        img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
        cv2.line(img, (center[0], 0), (center[0], resolution[1]), 255, brush_size)
        straight.append(img)
    masks[0] = straight
    return masks

