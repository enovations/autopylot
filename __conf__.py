###############################
#       FLASK SETTINGS        #
###############################
run_flask = True # set to False to disable flask
flask_port = 1234
flask_threaded = True

###############################
#       ROBOT SETTINGS        #
###############################
v = 0.25  # speed of robot in m/s

# coordinate system calibration
pixel_25cm_distance = 40
first_cut_to_image_edge_in_pixels = 17
meter_to_pixel_ratio = 0.25 / pixel_25cm_distance  # ratio of pixels on screen to meters in real world
position_gain = -0.05

angularvel_factor_p = 50
tx, ty, wi = 248, 117, 265  # transformation result offset x, offset y and length of square
orig_sqre = [[219, 146], [602, 145], [528, 402], [244, 403]]  # original map of pixels: define in clockwise direction
