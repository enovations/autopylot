###############################
#       FLASK SETTINGS        #
###############################
run_flask = True  # set to False to disable flask
flask_port = 1234
flask_threaded = True

###############################
#       ROBOT SETTINGS        #
###############################
v = 0.05  # speed of robot in m/s
meter_to_pixel_ratio = 0.25 / 20  # ration of pixels on screen to meters in real world
angularvel_factor_p = 50
tx, ty, wi = 248, 117, 265 # transformation result offset x, offset y and length of square
orig_sqre = [[219, 146], [602, 145], [528, 402], [244, 403]] # original map of pixels: define in clockwise direction
