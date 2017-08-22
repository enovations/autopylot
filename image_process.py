import cv2
import numpy as np


def transform_image(image):
    w, h = 1000, 750
    img = cv2.resize(image, (w, h))
    m_rot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
    img = cv2.warpAffine(img, m_rot, (w, h))
    pts1 = np.float32([[178, 95], [522, 100], [32, 275], [511, 288]])
    pts2 = np.float32([[177, 95], [401, 98], [178, 318], [398, 316]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img = cv2.warpPerspective(img, matrix, (w, h))

    return img


def crop_image(image):
    return image[350:550, 150:600]


def threshold_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 11)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 401, 10)
    return img
