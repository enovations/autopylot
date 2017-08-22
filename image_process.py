import cv2
import numpy as np


def transform_image(img):

    w, h = img.size

    # rotate image
    m_rot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
    img = cv2.warpAffine(img, m_rot, (w, h))

    #transform image
    ow, oh = 205, 0
    wi = 180
    pts1 = np.float32([[153, 169], [427, 170], [486, 359], [61, 357]])
    pts2 = np.float32([[ow, oh+wi], [ow+wi, oh+wi], [ow+wi, oh], [ow, oh]])
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
    # cv2.erode(img, None, dst=img, iterations=5)
    return img


def resize(image):
    return cv2.resize(image, (113, 50))
