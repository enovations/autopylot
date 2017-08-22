import cv2
import numpy as np


def transform_image(img):

    w, h = 640, 480

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

    m_rot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
    img = cv2.warpAffine(img, m_rot, (w, h))

    return img


def crop_and_resize_image(image):
    img = cv2.resize(image, (160, 120))
    return img[60:120, 0:160]


def threshold_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 4)

    mask = cv2.imread('res/mask.png')
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    img = cv2.bitwise_and(img, mask)

    return img
