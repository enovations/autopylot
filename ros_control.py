noros = False

try:
    import rospy
    from geometry_msgs.msg import Twist, Transform, Pose, PoseStamped, Point, Point32, PointStamped, Vector3, Quaternion
except:
    noros = True

robot_pub = None


def init():
    global robot_pub
    if not noros:
        print('ros is hererererere!!!')
        rospy.init_node('autopylot', anonymous=True)
        robot_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=0)
        pntlt_pub = rospy.Publisher('/pan_tilt/cmd_vel', Twist, queue_size=0)


def update_robot(v, w):
    print(v, w)

    if noros:
        return

    global robot_pub

    message = Twist(Vector3(float(v), 0, 0), Vector3(0, 0, float(w)))
    robot_pub.publish(message)
