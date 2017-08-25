import socket

client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
client.connect('/tmp/autopylot_input_socket')

while True:
    dest = input('select dest: ')
    client.send(dest.encode('utf8'))


@atexit.register
def stop():
    client.close()
