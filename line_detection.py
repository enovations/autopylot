import cv2


def evaluate(img1, img2):
    img = cv2.bitwise_and(img1, img2)
    return cv2.countNonZero(img), img


def get_radius(image, masks):
    r, s = 0, 0
    bimg = image
    for k in masks.keys():
        for mask in masks[k]:
            res, img = evaluate(image, mask)
            if res > s:
                s, r = res, k
                bimg = img
    return r, bimg
