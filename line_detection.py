import cv2


def evaluate(img1, img2):
    img = cv2.bitwise_and(img1, img2)
    return cv2.countNonZero(img), img


def get_radius(image, masks):
    r, s, position = 0, 0, 0
    bimg = image
    for k in masks.keys():
        for i in range(len(masks[k])):
            res, img = evaluate(image, masks[k][i])
            if res > s:
                r, s, position = k, res, i
                bimg = img

    position -= len(masks[0]) // 2
    position /= len(masks[0]) // 2
    position = abs(position) + 0.5
    return r*position, bimg
