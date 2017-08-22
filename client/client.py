import io
import socket
import struct
import cv2
import numpy as np

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8063))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)

        img_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

        image = cv2.imdecode(img_array, 0)
        cv2.imshow("transformed_image", image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()


finally:
    connection.close()
    server_socket.close()