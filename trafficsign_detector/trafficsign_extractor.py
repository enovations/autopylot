import cv2
import numpy as np

import image_process

image = cv2.imread('known_signs/3.jpg')

image = image_process.transform_image(image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)

im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

for con in contours:
    rect = cv2.minAreaRect(con)
    box = cv2.boxPoints(rect)
    box = np.float32(box)

    matrix = cv2.getPerspectiveTransform(box, np.float32([[0, 0], [0, 64], [64, 64], [64, 0]]))
    img = cv2.warpPerspective(image, matrix, (64, 64))

    cv2.imshow("img", img)
    cv2.waitKey(0)
