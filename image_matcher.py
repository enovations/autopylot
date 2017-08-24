import numpy as np
import cv2


def threshold_sign(img):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # img = cv2.medianBlur(img, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 4)

    return img


img = cv2.imread('trafficsign_detector/00/1_2.jpg')
