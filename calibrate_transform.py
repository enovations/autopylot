# this is a tool to calibrate transformation from sample.jpg
import cv2
import numpy as np

clicks1 = []
clicks = 0


def click(event, x, y, flags, param):
    global clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        clicks += 1
        if clicks < 5:
            clicks1.append([x, y])
        else:
            print(clicks1)


w, h = 640, 480

# click on point in clockwise direction, first current, then desired shape
image = cv2.imread('sample1.jpg')

cv2.resize(image, (w, h))

cv2.namedWindow("image")
cv2.setMouseCallback("image", click)

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

ow, oh, wi = 248, 117, 265

# rotate image - probably not necessary
# m_rot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
# image = cv2.warpAffine(image, m_rot, (w, h))

# test
pts1 = np.float32(clicks1)
# pts1 = np.float32([[219, 146], [602, 145], [528, 402], [244, 403]])

matrix = cv2.getPerspectiveTransform(
    pts1,
    np.float32([[ow, oh + wi], [ow + wi, oh + wi], [ow + wi, oh], [ow, oh]])
)
image = cv2.warpPerspective(image, matrix, (w, h))

cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
