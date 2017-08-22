import cv2
import numpy as np


def transform_image(image):
    # rotate and transform image
    w, h = 640, 480
    Mrot = cv2.getRotationMatrix2D((w / 2, h / 2), 180, 1.0)
    image = cv2.warpAffine(image, Mrot, (w, h))
    pts1 = np.float32([[178, 95], [522, 100], [32, 275], [511, 288]])
    pts2 = np.float32([[177, 95], [401, 98], [178, 318], [398, 316]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    image = cv2.warpPerspective(image, M, (w, h))
    return image
