![autopylot](http://i.imgur.com/HxtNn33.gif)

This is our best autopylot yet. It finds a line and follows it, obeys traffic signs and is a good driver. It can also drive you to the desired destination. It uses OpenCV and tensorflow neural netwrok for traffic sign detection.

# Features

- script runs and exits if you use force exit command
- multithreaded opencv image process preview in browser on port 1234
- single line curve detection and adaption

# Dependencies

- opencv
- numpy (comes with opencv)
- (OPTIONAL: for traffic sign detection) tensorflow
- (OPTIONAL: for opencv preview in browser) flask
- (OPTIONAL: for use on actual Raspberry Pi) picamera
- (OPTIONAL: for use on actual Raspberry Pi with ROS) rospy

OPTIONAL libraries are not required. The code runs even without them, but some of the functions are ignored in such case. Without picamera, it uses sample.jpg for processing, without rospy, there is no control, but the commands are printed in console, without flask, there is no preview in browser.

# Running on Raspberry Pi

You need to run both main.py (on Python 3) and ros_server.py (on Python 2). They communicate using unix socket. On test environment, if there is no unix socket, data is not sent.

# Appendix

![SLOTH](https://i.ytimg.com/vi/mkQzYyi25sA/maxresdefault.jpg)
