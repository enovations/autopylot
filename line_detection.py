import cv2


def evaluate(img1, img2):
    img = cv2.bitwise_and(img1, img2)
    return cv2.countNonZero(img)


def get_radius(image, masks):
    r, s = 0, 0
    for k in masks.keys():
        res = evaluate(image, masks[k])
        if res > s: s, r = res, k
    return r
