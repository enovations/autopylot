# import the necessary packages
# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import cv2
import numpy as np

# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# rawCapture = PiRGBArray(camera)

# # allow the camera to warmup
# time.sleep(0.1)

# # grab an image from the camera
# camera.capture(rawCapture, format='bgr')
# img = rawCapture.array

img = cv2.imread('sample.jpg')

# transform
w, h = 640, 480
Mrot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
img = cv2.warpAffine(img, Mrot, (w, h))
pts1 = np.float32([[178, 95], [522, 100], [32, 275], [511, 288]])
pts2 = np.float32([[177, 95], [401, 98], [178, 318], [398, 316]])
M = cv2.getPerspectiveTransform(pts1, pts2)
img = cv2.warpPerspective(img, M, (w, h))

# blur
img = cv2.medianBlur(img, 5)

cv2.imshow('image', img)
cv2.waitKey(0)

# threshold
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY, 11, 2)

cv2.imwrite('neki.jpg', img)
