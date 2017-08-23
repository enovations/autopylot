![autopylot](http://i.imgur.com/HxtNn33.gif)

This is our best autopylot yet. It finds a line and follows it. Probaby. Don't know yet. Have written some code but didn't test it yet.

# Features

- script runs and exits if you use force exit command
- multithreaded opencv image process preview in browser on port 1234
- single line curve detection and adaption

# Dependencies

- opencv
- numpy (comes with opencv)
- (OPTIONAL: for opencv preview in browser) flask
- (OPTIONAL: for use on actual Raspberry Pi) picamera
- (OPTIONAL: for use on actual Raspberry Pi with ROS) rospy

OPTIONAL libraries are not required. The code runs even without them, but some of the functions are ignored in such case. Without picamera, it uses sample.jpg for processing, without rospy, there is no control, but the commands are printed in console, without flask, there is no preview in browser.

# Appendix

![SLOTH](https://i.ytimg.com/vi/mkQzYyi25sA/maxresdefault.jpg)
