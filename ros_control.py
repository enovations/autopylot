import socket

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
    global client
    if not nounix:
        client.send(str(v) + ' ' + str(w))


def close():
    global client
    if not nounix:
        client.close()
