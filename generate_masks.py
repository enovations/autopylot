import numpy as np
import cv2

def get_masks(resolution=(113, 50)):
    brush_size = int(5 / 113 * resolution[0])
    min_rad = int(resolution[0] * 0.16)
    max_rad = int(resolution[0] * 5.31)

    center = (resolution[0] // 2, resolution[1])

    masks = {}
    step = 2
    r = min_rad
    while r <= max_rad:
        # create left arc18
        img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
        cv2.circle(img, (center[0] - r, center[1]), r, 255, brush_size)
        masks[r] = img

        # create right arc
        img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
        cv2.circle(img, (center[0] + r, center[1]), r, 255, brush_size)
        masks[r] = img

        r += step
        step = int(step * 1.5)

    # create straight line
    img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
    cv2.line(img, (center[0], 0), (center[0], resolution[1]), 255, brush_size)
    masks[0] = img
    return masks

