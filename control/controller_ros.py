import socket

import __conf__

nounix = False

try:
    socket.AF_UNIX
except:
    nounix = True

client = None


def init():
    global client

    if not nounix:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        client.connect('/tmp/autopylot_socket')


def update_robot(v, w):
    if w > __conf__.max_w: w = __conf__.max_w
    if w < -__conf__.max_w: w = -__conf__.max_w
    if v > __conf__.max_speed: v = __conf__.max_speed

    global client
    if not nounix:
        message = str(v) + ' ' + str(w)
        client.send(message.encode('utf8'))


def close():
    global client
    if not nounix:
        client.close()
