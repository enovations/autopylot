import cv2
import __conf__


def evaluate(img1, img2):
    img = cv2.bitwise_and(img1, img2)
    return cv2.countNonZero(img), img

def r_diff(r1, r2):
    r1, r2 = r1*__conf__.meter_to_pixel_ratio, r2*__conf__.meter_to_pixel_ratio
    if r1 == 0 and r2 == 0: return 0
    if r1 == 0: return abs(1/r2)
    if r2 == 0: return abs(1/r1)

    return abs(1/r1 - 1/r2)


def detect(image, masks):
    matches = []

    for k in masks.keys():
        for i in range(len(masks[k])):
            res, img = evaluate(image, masks[k][i])
            if res >= __conf__.min_line_match:

                position = i
                position -= len(masks[0]) // 2
                position *= 160 // __conf__.num_of_mask_offsets

                if __conf__.run_flask:
                    matches.append([k, res, position, img, masks[k][i]])  # r, s, position, bimg, mask
                else:
                    matches.append([k, res, position])  # r, s, position

    matches.sort(key=lambda x: x[1], reverse=True)

    if len(matches) > 0:
        result = [matches[0]]

        if len(matches) > 1:
            for i in range(1, len(matches)):
                if r_diff(result[0][0], matches[i][0]) >= __conf__.min_split_r:
                    result.append(matches[i])
                    break
    else: result = []
    return result
