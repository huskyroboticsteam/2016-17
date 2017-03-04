import socket
import sys

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind(('192.168.0.10', 24))
while True:
    try:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("Shit: {0}\n".format(data))
    except socket.error:
        pass

