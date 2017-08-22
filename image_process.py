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


def treshold_image(image):
    img = image
    for j in range(len(img)):
        for i in range(len(img[j])):
            pixel = img[j][i]
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                for p in range(3):
                    img[j][i][p] = 255

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img, 11)
    # ret, img = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 35, 3)
    return img
