from PyQt4 import QtCore, QtGui
import socket, struct
import joystick


class CommsUpdate(QtGui.QWidget):

    ROVER_HOST = "192.168.0.50"
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
            self.timer.start(10)

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
        # print self.joy.joystick_axis[0][0]

        throttle = self.joy.joystick_axis[0][1]
        steering = self.joy.joystick_axis[0][0]

        throttle = translateValue(throttle, -32768, 32768, 255, -255)
        steering = translateValue(steering, -32768, 32768, -100, 100)
        if abs(throttle) < 20:
            throttle = 0
        if abs(steering) < 20:
            steering = 0
        print throttle, steering

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<?hh", self.auto, int(throttle), int(steering))

        try:
            self.rover_sock.sendto(buff, (self.ROVER_HOST, self.ROVER_PORT))
        except:
            print "Failed to send"

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

            print lat, lng

            self.signalUpdate.emit((lat, lng))

            # TODO: add arm packets structure


# translate values from one range to another
def translateValue(value, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valueScaled * outSpan)
