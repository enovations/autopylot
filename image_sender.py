# import io
# import socket
# import struct
# import cv2
#
# client_socket = socket.socket()
# client_socket.connect(('localhost', 8063))
#
# def send(image):
#     try:
#
#         connection = client_socket.makefile('wb')
#         stream = io.BytesIO()
#
#         # stream = cv2.imencode('.jpg', image)
#
#         # Write the length of the capture to the stream and flush to  # ensure it actually gets sent
#         connection.write(struct.pack('<L', stream.tell()))
#         connection.flush()
#
#         # Rewind the stream and send the image data over the wire
#         stream.seek(0)
#         connection.write(stream.read())
#
#         # Reset the stream for the next capture
#         stream.seek(0)
#         stream.truncate()
#         # Write a length of zero to the stream to signal we're done
#         connection.write(struct.pack('<L', 0))
#     finally:
#         connection.close()
#         client_socket.close()

import socket
import pickle

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))


def send(image):
    data = pickle.dumps(image)

    clientsocket.send("H" + len(data))
    clientsocket.send("A")
    clientsocket.send(data)
