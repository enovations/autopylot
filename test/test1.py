# first test py

import cv2
import numpy as np


def click_and_crop(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


w, h = 1000, 750

origimg = cv2.imread('../sample.jpg')

resizedimg = cv2.resize(origimg, (w, h))

Mrot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
img = cv2.warpAffine(resizedimg, Mrot, (w, h))

pts1 = np.float32([[178, 95], [522, 100], [32, 275], [511, 288]])
pts2 = np.float32([[177, 95], [401, 98], [178, 318], [398, 316]])

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (w, h))

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

cv2.imshow('image', dst)
cv2.waitKey(0)
