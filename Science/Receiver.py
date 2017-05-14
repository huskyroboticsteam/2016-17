import sys
import socket


LISTEN = True



SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if LISTEN:
    SOCKET.bind(('192.168.0.2', 22))
    while True:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("\nData Received: " + str(data) + "\n\tFrom: " + str(clientAddr))
