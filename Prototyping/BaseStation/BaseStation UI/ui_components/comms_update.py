from PyQt4 import QtCore
import socket
import struct
import joystick


class ConnectionManager:
    def __init__(self):
        self.ROVER_HOST = "192.168.0.50"
        self.ARM_HOST = "192.168.0.90"  # For over ethernet
        # self.ARM_HOST = "192.168.7.2" # 7.2 for over USB
        self.LOCAL_HOST = "127.0.0.1"
        self.ROVER_TCP_PORT = 8841
        self.ROVER_PORT = 8840
        self.ARM_PORT = 53204
        self.SCIENCE_PORT = 5000

        self.auto = AutonomousConnection(self.ROVER_HOST, self.ROVER_TCP_PORT)
        # Kill the thread when the work is done
        self.auto.finished.connect(self.auto.quit)

        self.drive = DriveConnection(self.ROVER_HOST, self.ROVER_PORT, 2) # Last param specifies joystick number
        self.drive.start()

        self.arm = ArmConnection(self.ARM_HOST, self.ARM_PORT, 3)
        self.arm.start()

        self.science = ScienceConnection("192.168.0.1", self.SCIENCE_PORT)
        self.science.start()

    def enable_tcp(self, enable):
        if enable:
            self.auto.start()

    # Safely close all threads and sockets
    def shutdown(self):
        # Close the socket then kill the thread
        if self.auto.auto_sock is not None:
            self.auto.auto_sock.shutdown(socket.SHUT_RDWR)
            self.auto.auto_sock.close()
        self.auto.quit()

        if self.science.science_sock is not None:
            self.science.science_sock.close()
        self.science.quit()

        # Kill the thread
        self.drive.quit()

        self.arm.killing = True
        self.arm.kill()
        self.arm.quit()


# TODO conform to python's conventions for abstract classes instead of passing with a comment
class UdpConnection(QtCore.QThread):
    def __init__(self, host, port):
        QtCore.QThread.__init__(self)

        self.host = host
        self.port = port

        # UDP connection to the rover
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

    # Subclasses implement this!!
    def send_message(self):
        pass

    def receive_message(self):
        pass

    def run(self):
        while True:
            self.send_message()
            self.receive_message()
            self.msleep(10)


class DriveConnection(UdpConnection):
    sensorUpdate = QtCore.pyqtSignal([dict])
    gpsUpdate = QtCore.pyqtSignal([tuple])

    def __init__(self, host, port, joystick_control_index):
        UdpConnection.__init__(self, host, port)

        # Indicates whether the rovers is in autonomous mode
        self.auto = False

        # Indicates whether emergency stop has been pressed (CANNOT BE UNDONE)
        # Reset the UI if emergency stopped
        self.stop = False
        self.joystick_control_index = joystick_control_index

        self.joys = joystick.getJoysticks()
        self.joys.start()

        self.timer = None

    def enable_tcp(self, enable):
        self.auto = enable

    def stopping(self):
        if self.stop:
            self.stop = False
            print "Starting"
        else:
            print "Stopping"
            self.stop = True

    def send_message(self):
        """
        Sends the rover throttle and steering information from joystick axises
        :return: None
        """

        throttle = 0
        steering = 0

        #print self.joys.joystick_control
        #print self.joys.joystick_axis

        try:
            # Emit drive of zero if emergency stop isn't enabled
            if self.stop is False and self.joys.joystick_control[self.joystick_control_index] is not None:
                throttle = self.joys.joystick_axis[self.joys.joystick_control[self.joystick_control_index]][1]
                steering = self.joys.joystick_axis[self.joys.joystick_control[self.joystick_control_index]][0]
        except:
            pass
        else:
            throttle = translateValue(throttle, -32768, 32768, 255, -255)
            steering = translateValue(steering, -32768, 32768, -100, 100)
            if abs(throttle) < 20:
                throttle = 0
            if abs(steering) < 20:
                steering = 0

            # print throttle, steering

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<?hh", self.auto, int(throttle), int(steering))

        # Will send even if we can't reach the rover?
        self.sock.sendto(buff, (self.host, self.port))

    def receive_message(self):
        """
        Receive the incoming UDP packets, unpack them and emit them so other UI components can use them
        :return: Emit a dictionary of sensor values
        :return: Emit a tuple of lat lng coordinates
        """

        try:
            rover_data = self.sock.recv(1024)
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
                          "Drive Encoder 1": str(enc_1), "Drive Encoder 2": str(enc_2), "Drive Encoder 3": str(enc_3),
                          "Drive Encoder 4": str(enc_4)}

            self.sensorUpdate.emit(dictionary)
            self.gpsUpdate.emit((lat, lng))


class ArmConnection(UdpConnection):
    def __init__(self, host, port, joystick_control_index):
        super(self.__class__, self).__init__(host, port)
        # Make this joystick # 2
        self.joys = joystick.getJoysticks()
        self.joys.start()

        self.killing = False

        self.joystick_control_index = joystick_control_index

    def kill(self):
        for i in xrange(6):
            buff = struct.pack("<ffffff", 0, 0, 0, 0, 0, 0)
            self.sock.sendto(buff, (self.host, self.port))

    def send_message(self):
        if not self.joys.ready:
            return
        # Don't run if joystick not plugged in
        if self.joys.joystick_control[self.joystick_control_index] is None or self.killing:
            # print "Arm joystick not plugged in"
            return

        # These mappings are for my Logitech F710 controller. 
        # Change accordingly if your controller is different
        base_rotation = self._base_axis(2, 5) / -2 # Triggers
        shoulder = - self._joy_axis(1) / 2  # Left stick Y axis
        wrist_lift = self._joy_axis(4) / -2 # Right stick Y axis
        elbow = self._button_axis(2, 0) / 2 # X- open hand, A- Close hand. (x left, a bottom)
        wrist_rotation = self._button_axis(4, 5) / -4 # Bumpers
        hand_grip = self._button_axis(1, 3) # B is down, Y is up (B is right, Y is up)
        winch = self._joy_axis(0) / 5

        buff = struct.pack("<fffffff", base_rotation, shoulder, elbow, wrist_lift, wrist_rotation, hand_grip, winch)

        print (base_rotation, shoulder, elbow, wrist_lift, wrist_rotation, hand_grip, winch)

        # Will send even if we can't reach the rover?
        self.sock.sendto(buff, (self.host, self.port))

    def _joy_axis(self, axisNum):
        """
        Returns the value at the specificed joystick axis. The value will be on
        the scale of 0-1.
        """
        val = self.joys.joystick_axis[self.joys.joystick_control[self.joystick_control_index]][axisNum]
        val /= 32768.0 # Scale to -1 .. 1

        # Deadzone
        return 0 if (abs(val) < .10) else val

    def _base_axis(self, axisNum, axis2Num):
        """
        Returns the value at the specificed joystick axis. The value will be on
        the scale of 0-1.
        """
        # print self.joys.joystick_control
        # print self.joystick_control_index
        val = self.joys.joystick_axis[self.joys.joystick_control[self.joystick_control_index]][axisNum]
        val2 = self.joys.joystick_axis[self.joys.joystick_control[self.joystick_control_index]][axis2Num]
        val /= 32768.0 # Scale to -1 .. 1
        val2 /= 32768.0

        # Deadzone
        if val < 0.10 and val2 < 0.10:
            return 0
        if val < 0.10:
            return val2
        if val2 < 0.10:
            return -val
        else:
            return 0

    def _button_axis(self, forwardBtn, reverseBtn):
        if self.joys.joystick_button[self.joys.joystick_control[self.joystick_control_index]][forwardBtn]:
            return 1.0
        elif self.joys.joystick_button[self.joys.joystick_control[self.joystick_control_index]][reverseBtn]:
            return -1.0
        else:
            return 0


class ScienceConnection(QtCore.QThread):
    sensorUpdate = QtCore.pyqtSignal([dict])

    def __init__(self, host, port):
        super(self.__class__, self).__init__()

        self.host = host
        self.port = port
        self.science_sock = None
        self.client = None

    def run(self):
        self.bind()

        while True:
            self.science_sock.listen(1)
            client, addr = self.science_sock.accept()
            self.client = client
            self.receive_message()
            self.msleep(1)

    def bind(self):
            self.science_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.science_sock.bind((self.host, self.port))

    def send_picture(self, check_state):
        if check_state:
            buff = struct.pack(">ic18sc", 0, '\x80', "I can haz picture?", '\x02')
        else:
            buff = struct.pack(">ic18sc", 0, '\x80', "I can haz picture?", '\x01')

        if self.client is not None:
            self.client.send(buff)

    def send_sliders(self, value, name):
        value = int(value)
        if name == "arm":
            buff = struct.pack('>Icci', 0, '\x81', '\x03', value)
        elif name == "speed":
            buff = struct.pack('>Icci', 0, '\x81', '\x01', value)
        elif name == "cam":
            buff = struct.pack('>Icci', 0, '\x81', '\x02', value)
        elif name == "cup":
            buff = struct.pack('>Icci', 0, '\x81', '\x04', value)
        elif name == "pos":
            print "here"
            buff = struct.pack('>Icci', 0, '\x81', '\x00', value)
        elif name == "release":
            buff = struct.pack('>Icci', 0, '\x81', '\x00', value)

        if self.client is not None:
            print "Lel"
            self.client.send(buff)

    def receive_message(self):
        """
        Receive the incoming UDP packets, unpack them and emit them so other UI components can use them
        :return: Emit a dictionary of sensor values
        :return: Emit a tuple of lat lng coordinates
        """

        try:

            science_data = self.client.recv(1024)
        except socket.error:
            pass
        else:
            # Unpack the first six floats of the packet
            tup = struct.unpack_from(">Ic", science_data, 0)
            ide = tup[1]

            print tup

            if ide == '\x00':

                tup = struct.unpack_from(">HIhhH", science_data, 5)
                distance = tup[0]
                uv = tup[1]
                thermo_ext = tup[2]
                thermo_int = tup[3]
                humidity = tup[4]
                dictionary = {"Distance": str(distance), "UV": str(uv),
                              "Thermo Internal": str(thermo_ext), "Thermo External": str(thermo_int),
                              "Humidity": str(humidity)}
                self.sensorUpdate.emit(dictionary)
            elif ide == '\x01':
                tup = struct.unpack_from(">H", science_data, 5)
                stri = "Science "
                if tup == '\x00\x00':
                    print stri + "Okay"
                elif tup == '\x00\x01':
                    print stri + "Can't init ADC"
                elif tup == '\x00\x02':
                    print stri + "Can't setup DIO"
                elif tup == '\x00\x03':
                    print stri + "Can't read DIO"
                elif tup == '\x00\x04':
                    print stri + "Not Init Servo"
                elif tup == '\x00\xFE':
                    print stri + "Ping Errors"
                elif tup == '\x00\xFF':
                    print stri + "Unknown Error"
                elif tup == '\x01\x01':
                    print stri + "Thermo No Reading"
                elif tup == '\x01\x02':
                    print stri + "Thermo No Internal Reading"
                elif tup == '\x01\x03':
                    print stri + "Thermo Reading Invalid"
                elif tup == '\x01\x04':
                    print stri + "Thermo Open Circuit"
                elif tup == '\x01\x05':
                    print stri + "Thermo GND Short"
                elif tup == '\x01\x06':
                    print stri + "Thermo VCC Short"
                elif tup == '\x01\x07':
                    print stri + "Thermo General Failure"
                elif tup == '\x01\x08':
                    print stri + "Comm Failure"
                elif tup == '\x02\x01':
                    print stri + "UV No Reading"
                elif tup == '\x02\x02':
                    print stri + "UV Reading Invalid"
                elif tup == '\x02\x03':
                    print stri + "UV Comm Failure"
                elif tup == '\x03\x01':
                    print stri + "Distance No Reading"
                elif tup == '\x03\x02':
                    print stri + "Distance Reading Invalid"
                elif tup == '\x03\x03':
                    print stri + "Distance Comm Failure"
                elif tup == '\x03\x04':
                    print stri + "Distance Failed Begin Ranging"
                elif tup == '\x03\x05':
                    print stri + "Distance Failed Stop Ranging"
                elif tup == '\x04\x01':
                    print stri + "Hum No Reading"
                elif tup == '\x04\x02':
                    print stri + "Hum Reading Invalid"
                elif tup == '\x04\x03':
                    print stri + "Hum Overzealous Insertion"
                elif tup == '\x04\x04':
                    print stri + "Hum Comm Failure"
                elif tup == '\x05\x01':
                    print stri + "Comms Can't Init"
                elif tup == '\x05\x02':
                    print stri + "Comms Failed To Start Receive"
                elif tup == '\x05\x03':
                    print stri + "Comms Failed to Send Packet"
                elif tup == '\x05\x04':
                    print stri + "Comms Failed to Parse Packet"
                elif tup == '\x05\x05':
                    print stri + "Comms Invalid Request"

            elif ide == '\x02':
                tup = struct.unpack_from(">hhh?", science_data, 5)
                enc1 = tup[0]
                enc2 = tup[1]
                enc3 = tup[2]
                limit = tup[3]
                dictionary = {"Science Encoder 1": str(enc1), "Science Encoder 2": str(enc2),
                              "Science Encoder 3": str(enc3), "Limit Switch": str(limit)}
                self.sensorUpdate.emit(dictionary)


# Open a TCP connect in a separate thread
class AutonomousConnection(QtCore.QThread):
    requestMarkers = QtCore.pyqtSignal()
    tcp_enabled = QtCore.pyqtSignal(bool)

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
            print "Failed to Connect to Drive Over TCP"
            self.tcp_enabled.emit(False)
        else:
            self.tcp_enabled.emit(True)
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
            self.auto_sock.shutdown(socket.SHUT_RDWR)
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
