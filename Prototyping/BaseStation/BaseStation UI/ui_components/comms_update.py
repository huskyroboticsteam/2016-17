from PyQt4 import QtCore
import socket
import struct
import joystickv1


class ConnectionManager:
    def __init__(self):

        self.ROVER_HOST = "192.168.0.50"
        self.LOCAL_HOST = "127.0.0.1"
        self.ROVER_TCP_PORT = 8841
        self.ROVER_PORT = 8840

        self.tcp = TCPConnection(self.ROVER_HOST, self.ROVER_TCP_PORT)
        # Kill the thread when the work is done
        self.tcp.finished.connect(self.tcp.quit)

        self.drive = DriveConnection(self.ROVER_HOST, self.ROVER_PORT)
        self.drive.start()

    def enable_tcp(self, enable):
        if enable:
            self.tcp.start()

    # Safely close all threads
    def shutdown(self):
        self.tcp.quit()
        self.drive.quit()


class DriveConnection(QtCore.QThread):

    sensorUpdate = QtCore.pyqtSignal([dict])
    gpsUpdate = QtCore.pyqtSignal([tuple])

    def __init__(self, host, port):
        super(self.__class__, self).__init__()

        # Indicates whether the rovers is in autonomous mode
        self.auto = False
        self.ROVER_HOST = host
        self.ROVER_PORT = port

        # Indicates whether emergency stop has been pressed (CANNOT BE UNDONE)
        # Reset the UI if emergency stopped
        self.stop = False

        self.joys = joystickv1.Joystick()
        self.joys.start()

        # UDP connection to the rover
        self.rover_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rover_sock.setblocking(False)

        self.timer = None

    def run(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.send_message)
        self.timer.timeout.connect(self.receive_message)
        self.timer.start(10)

    def enable_tcp(self, enable):
        self.auto = enable

    def stopping(self):
        self.stop = True

    def send_message(self):
        """
        Sends the rover throttle and steering information from joystick axises
        :return: None
        """

        throttle = 0
        steering = 0

        try:
            throttle = self.joys.joystick_axis[0][1]
            steering = self.joys.joystick_axis[0][0]
        except:
            pass
        else:
            throttle = translateValue(throttle, -32768, 32768, 255, -255)
            steering = translateValue(steering, -32768, 32768, -100, 100)
            if abs(throttle) < 20:
                throttle = 0
            if abs(steering) < 20:
                steering = 0

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<?hh", self.auto, int(throttle), int(steering))

        # Will send even if we can't reach the rover?
        self.rover_sock.sendto(buff, (self.ROVER_HOST, self.ROVER_PORT))

    def receive_message(self):
        """
        Receive the incoming UDP packets, unpack them and emit them so other UI components can use them
        :return: Emit a dictionary of sensor values
        :return: Emit a tuple of lat lng coordinates
        """

        try:
            rover_data = self.rover_sock.recv(1024)
        except socket.error:
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

            self.sensorUpdate.emit(dictionary)
            self.gpsUpdate.emit((lat, lng))


# Open a TCP connect in a separate thread
class TCPConnection(QtCore.QThread):

    requestMarkers = QtCore.pyqtSignal()

    def __init__(self, host, port):
        super(self.__class__, self).__init__()

        self.ROVER_HOST = host
        self.ROVER_TCP_PORT = port
        self.auto_sock = None
        self.markers = []

    def set_markers(self, markers):
        self.markers = markers

    def run(self):
        # Ask the map for markers
        self.requestMarkers.emit()

        # TCP connection to the rover
        try:
            self.auto_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.auto_sock.connect((self.ROVER_HOST, self.ROVER_TCP_PORT))
        except socket.error:
            print "Failed to connect over TCP"
        else:
            # TODO: Emit some data allowing button label to change to enabled
            self.send_data()

    def send_data(self):
        for i in range(0, len(self.markers)):

            lat = float(self.markers[i][0])
            lng = float(self.markers[i][1])

            if i == len(self.markers) - 1:
                self.send_auto_mode(False, lat, lng)
            else:
                self.send_auto_mode(True, lat, lng)

        self.close_tcp()

    def send_auto_mode(self, more, lat, lng):

        # Put the first boolean value in the buffer
        buff = struct.pack("<?ff", more, lat, lng)
        self.auto_sock.send(buff)

    def close_tcp(self):
        if self.auto_sock is not None:
            self.auto_sock.close()
            self.auto_sock = None




# translate values from one range to another
def translateValue(value, inMin, inMax, outMin, outMax):
    """
    Linearly maps from one range to another range
    :param value: Input value to convert
    :param inMin: Bottom of the input range
    :param inMax: Top of the input range
    :param outMin: Bottom of the output range
    :param outMax: Top of the output range
    :return: Value scaled to the new range dimensions
    """
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valueScaled * outSpan)
