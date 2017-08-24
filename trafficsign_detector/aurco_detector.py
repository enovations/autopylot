import __conf__
import cv2.aruco as aruco


def detect_marker(image):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejected_points = aruco.detectMarkers(image, aruco_dict, parameters=parameters)

    res = []

    for i in range(len(ids)):
        if ids[i] not in __conf__.marker_ids:
            continue

        if corners[i][0] > corners[i][3]:
            res.append((ids[i], True))
        else:
            res.append((ids[i], False))
    return res
