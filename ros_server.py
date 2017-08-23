import rospy
import socket
from geometry_msgs.msg import Twist, Transform, Pose, PoseStamped, Point, Point32, PointStamped, Vector3, Quaternion


server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server.bind('/tmp/autopylot_socket')

rospy.init_node('slothface')
robot_pub = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=0)

rate = rospy.Rate(100)

while not rospy.is_shutdown():
    datagram = server.recv(1024)
    if not datagram:
        break

    v, w = datagram.decode('utf8').split()
    message = Twist(Vector3(float(v), 0, 0), Vector3(0, 0, float(w)))
    robot_pub.publish(message)

    rate.sleep()
