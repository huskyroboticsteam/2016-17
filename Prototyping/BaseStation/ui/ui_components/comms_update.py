from PyQt4 import QtCore, QtGui
import socket, struct
import joystick


class CommsUpdate(QtGui.QWidget):

    ROVER_HOST = "192.168.0.40"
    LOCAL_HOST = "127.0.0.1"
    ROVER_PORT = 8840

    ROVER_TCP_PORT = 8841

    signalStatus = QtCore.pyqtSignal([dict])
    signalUpdate = QtCore.pyqtSignal([tuple])

    def __init__(self):
        super(self.__class__,self).__init__()

        # Indicates whether the rovers is in autonomous mode
        self.auto = False

        # Indicates whether emergency stop has been pressed (CANNOT BE UNDONE)
        # Reset the UI if emergency stopped
        self.stop = False

        self.joy = joystick.Joystick()

        try:
            # UDP connection to the rover
            self.rover_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.rover_sock.setblocking(False)

        except socket.error():
            print "Can't connect to rover"

        # Do this code if there was no exception in connecting
        else:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.send_message)
            self.timer.timeout.connect(self.receive_message)
            self.timer.start(500)

    def stopping(self):
        self.stop = True

    def shutdown(self):
        self.rover_sock.close()

    def open_tcp(self):
        # TCP connection to the rover
        self.auto_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.auto_sock.connect((self.ROVER_HOST, self.ROVER_TCP_PORT))

    def close_tcp(self):
        self.auto_sock.close()

    def send_message(self):

        throttle = self.joy.joystick_axis[0][0]
        steering = self.joy.joystick_axis[0][2]

        print throttle, steering

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<?hh", self.auto, throttle, steering)

        try:
            self.rover_sock.sendto(buff, (self.ROVER_HOST, self.ROVER_PORT))
        except:
            pass

        # TODO: Add sending code for the arm

    def send_auto_mode(self, more, lat, lng):

        # Put the first boolean value in the buffer
        buff = struct.pack("<?ff", more, lat, lng)

        self.auto_sock.send(buff)

    def receive_message(self):

        try:
            rover_data = self.rover_sock.recv(1024)
        except:
            # Do nothing
            pass
        else:
            # Unpack the first six floats of the packet
            tup = struct.unpack_from("<ffffffff", rover_data, 0)
            pot = tup[0]
            mag = tup[1]
            enc_1 = tup[2]
            enc_2 = tup[3]
            enc_3 = tup[4]
            enc_4 = tup[5]
            lat = tup[6]
            lng = tup[7]

            dictionary = {"Potentiometer": str(pot), "Magnetometer": str(mag),
                          "Encoder 1": str(enc_1), "Encoder 2": str(enc_2), "Encoder 3": str(enc_3), "Encoder 4": str(enc_4)}

            self.signalStatus.emit(dictionary)

            self.signalUpdate.emit((lat, lng))

        # TODO: add arm packets structure
