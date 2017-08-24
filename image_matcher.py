import numpy as np
import cv2
from matplotlib import pyplot as plt
import image_process

sign = np.uint8(cv2.imread('trafficsign_detector/known_signs/orig/avon.jpg', 0))
img = np.uint8(cv2.imread('trafficsign_detector/known_signs/13_0.jpg', 0))  # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(sign, None)
kp2, des2 = sift.detectAndCompute(img, None)


# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)
# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]


# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.7 * n.distance:
        matchesMask[i] = [1, 0]
draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)

img3 = cv2.drawMatchesKnn(sign, kp1, img, kp2, matches, None, **draw_params)
plt.imshow(img3, ), plt.show()
