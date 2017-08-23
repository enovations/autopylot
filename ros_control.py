noros = False

try:
    import rospy
    from geometry_msgs.msg import Twist, Transform, Pose, PoseStamped, Point, Point32, PointStamped, Vector3, Quaternion
except:
    noros = True


def init():
    if not noros:
        robot_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=0)
        pntlt_pub = rospy.Publisher('/pan_tilt/cmd_vel', Twist, queue_size=0)


def update_robot(v, w):
    pass
