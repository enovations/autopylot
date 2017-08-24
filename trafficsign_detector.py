import cv2
import numpy as np

templates = []


def load_templates():
    for i in range(0, 5):
        template = cv2.imread('signs/' + str(i) + '.jpg')

        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.adaptiveThreshold(template, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 5, 6)

        templates.append((i, template))

        for i2 in range(3):
            template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
            templates.append((i, template))


def match_image(image):
    curr_min = 1e20
    minx = -1

    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 5, 6)

    for template in templates:
        result = cv2.matchTemplate(image, templ=template[1], method=cv2.TM_SQDIFF)
        if curr_min > result:
            curr_min = result
            minx = template[0]

    return minx


def process_signs(signs):
    for sign in signs:
        print(match_image(sign))


def find_signs(image):
    gray = cv2.bilateralFilter(image, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # edged = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR)

    # cv2.drawContours(edged, contours, -1, (255, 255, 0), 4)

    x_offset = 0

    signs = []

    for con in contours:
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        box = np.float32(box)

        matrix = cv2.getPerspectiveTransform(box, np.float32([[0, 0], [0, 100], [100, 100], [100, 0]]))
        img_sign = cv2.warpPerspective(image, matrix, (100, 100))

        # edged[0:0 + img_sign.shape[0], x_offset:x_offset + img_sign.shape[1]] = img_sign

        signs.append(cv2.resize(img_sign, (48, 48)))

        # x_offset += 100

    process_signs(signs)
