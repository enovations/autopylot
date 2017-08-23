import cv2
import __conf__


def evaluate(img1, img2):
    img = cv2.bitwise_and(img1, img2)
    return cv2.countNonZero(img), img


def get_radius(image, masks):
    r, s, position = 0, 0, 0

    if __conf__.run_flask:
        bimg = image
        mask = image

    for k in masks.keys():
        for i in range(len(masks[k])):
            res, img = evaluate(image, masks[k][i])
            if res >= s:
                r, s, position = k, res, i

                if __conf__.run_flask:
                    bimg = img
                    mask = masks[k][i]

    position -= len(masks[0]) // 2
    position /= len(masks[0]) // 2
    position = abs(position) + 0.5

    if __conf__.run_flask:
        return r * position, s, bimg, mask
    else:
        return r * position, s
