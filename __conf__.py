import numpy as np

###############################
#       FLASK SETTINGS        #
###############################
run_flask = True # set to False to disable flask
flask_port = 1234
flask_threaded = True

###############################
#       ROBOT SETTINGS        #
###############################
max_speed = 1.5
max_w = 0.3
ar_max = 0.1
accel_filter_factor = 0.18
deccl_filter_factor = 0.35

# coordinate system calibration
pixel_25cm_distance = 40
first_cut_to_image_edge_in_pixels = 17
meter_to_pixel_ratio = 0.25 / pixel_25cm_distance  # ratio of pixels on screen to meters in real world
position_gain = -0.1
num_of_mask_offsets = 10
angularvel_factor_p = 50

tx, ty, wi = 248, 117, 265  # transformation result offset x, offset y and length of square
orig_sqre = [[219, 146], [602, 145], [528, 402], [244, 403]]  # original map of pixels: define in clockwise direction
pts1 = np.float32(orig_sqre)
pts2 = np.float32([[tx, ty + wi], [tx + wi, ty + wi], [tx + wi, ty], [tx, ty]])

full_dim = (640, 480)
proc_dim = (160, 120)

# line detection bounds
min_line_match = 85
min_match_ratio = 0.9
min_split_r = 0.5