import __conf__
import socket

client = None


def init():
    global client
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.connect('/tmp/autopylot_socket')


def update_robot(v, w):
    global client
    client.send(str(v) + ' ' + str(w))


def close():
    global client
    client.close()
