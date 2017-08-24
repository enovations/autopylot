import __conf__
import cv2.aruco as aruco
import cv2


def detect_marker(image):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejected_points = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    res = []

    if ids is None:
        return []

    for i in range(len(ids)):
        if ids[i][0] not in __conf__.marker_ids:
            continue

        if corners[i][0][0][1] < corners[i][0][3][1]:
            res.append((ids[i][0], True))
        else:
            res.append((ids[i][0], False))
    return res


cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    res = detect_marker(img)
    print(res)
