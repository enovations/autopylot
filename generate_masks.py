import numpy as np
import cv2
import __conf__

def get_masks(resolution=(160, 60)):
    brush_size = int(4 / 160 * resolution[0])
    min_rad = int(resolution[0] * 0.16) * 2
    max_rad = int(resolution[0] * 3.5)

    center = (resolution[0] // 2, resolution[1] + (2 * __conf__.pixel_25cm_distance - __conf__.first_cut_to_image_edge_in_pixels))

    masks = {}
    step = 2
    offset_step = 160 // __conf__.num_of_mask_offsets
    r = min_rad
    while r <= max_rad:
        # create left arc
        left = []
        for i in range(__conf__.num_of_mask_offsets):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (i*offset_step - r, center[1]), r, 255, brush_size)
            left.append(img)

        # create right arc
        rigth = []
        for i in range(__conf__.num_of_mask_offsets):
            img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
            cv2.circle(img, (i*offset_step + r, center[1]), r, 255, brush_size)
            rigth.append(img)

        masks[-r] = left
        masks[r] = rigth

        r += step
        step = int(step * 1.5)

    # create straight line
    straight = []
    for i in range(__conf__.num_of_mask_offsets):
        img = np.zeros((resolution[1], resolution[0]), dtype=np.uint8)
        cv2.line(img, (i*offset_step, 0), (i*offset_step, resolution[1]), 255, brush_size)
        straight.append(img)
    masks[0] = straight
    return masks

