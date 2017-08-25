import cv2

templates = []


def load_templates():
    for i in range(0, 6):
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

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 5, 6)

    for template in templates:
        result = cv2.matchTemplate(image, templ=template[1], method=cv2.TM_SQDIFF)
        if curr_min > result:
            curr_min = result
            minx = template[0]

    return minx, curr_min


def process_signs(signs):
    for sign in signs:
        id, val = match_image(sign)
        # if val < 25000000:
        #     print(id)
        # else:
        #     print('no sign!')
