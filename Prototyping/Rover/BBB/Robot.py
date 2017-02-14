import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import time
import PID
import math
import gps as GPS
import mag as MAG
import socket
import struct


class Robot:
    '''
    ROBOT motor configuration:

    Front
    +---+
    3   4
     \ /
      0
     / \
    1   2
    +---+
    Back
    '''

    def __init__(self):
        ADC.setup()
        # setup i2c to motorshield
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
        self.pwm.set_pwm_freq(60)
        self.mag = MAG.Magnetometer()
        self.gps = GPS.GPS()
        self.pot_pid = PID.PID(-0.1, 0, 0)
        # Potentiometer pin:
        self.POT_PIN = "AIN2"
        self.POT_LEFT = 0.771
        self.POT_RIGHT = 0.346
        self.POT_MIDDLE = (self.POT_LEFT + self.POT_RIGHT) / 2
        self.POT_TOL = 0.01
        # autopilot
        self.auto = True
        # list of GPS coords to travel to
        self.destinations = []
        self.receivedDrive = None
        self.robot_ip = "192.168.0.40"
        self.udp_port = 8840
        self.base_station_ip = None
        self.driveFormat = "<??hh"
        self.gpsFormat = "<?hhhhhh"
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.robot_ip, self.udp_port))
        self.sock.setblocking(False)


    # motor: throttle, F, B
    # 1: 8,  9,  10
    # 2: 13, 12, 11
    # 3: 2,  4,  3
    # 4: 7,  6,  5
    # drives the motor with a value, negative numbers for reverse
    def driveMotor(self, motor, motorVal):
        # verify value is good
        motorVal = int(motorVal)
        if abs(motorVal) > 255:
            print "bad value: " + str(motorVal)
            return
        # select proper pins
        if motor == 1:
            throttlePin = 8
            forwardPin = 9
            backPin = 10
        elif motor == 2:
            throttlePin = 13
            forwardPin = 12
            backPin = 11
        elif motor == 3:
            throttlePin = 2
            forwardPin = 4
            backPin = 3
        elif motor == 4:
            throttlePin = 7
            forwardPin = 6
            backPin = 5
        else:
            print "bad motor num"
            return
        self.pwm.set_pwm(forwardPin, 4096, 0)
        self.pwm.set_pwm(backPin, 4096, 0)
        self.pwm.set_pwm(throttlePin, 2048 - abs(motorVal) * 8, 2048 + abs(motorVal) * 8)
        if motorVal > 0:
            self.pwm.set_pwm(forwardPin, 0, 4096)
        if motorVal < 0:
            self.pwm.set_pwm(backPin, 0, 4096)
        print "driving motor: " + str(motor) + " with value: " + str(motorVal)


    # returns a float of how far from straight the potentiomer is. > 0 for Right, < 0 for left
    # returns -1 if error
    def readPot(self):
        result = self.POT_MIDDLE - ADC.read(self.POT_PIN)
        if result > self.POT_MIDDLE - self.POT_RIGHT or result < self.POT_MIDDLE - self.POT_LEFT:
            print result
            return -1
        return result

    # returns a 2-tuple of (throttle, turn)
    # turn value is 100 for full right -100 for full left and 0 for straight
    def getDriveParms(self, auto):
        if self.receivedDrive == None:
            return (0, 0)
        auto = self.receivedDrive[0]
        if auto:
            return (20, self.calculateDesiredTurn(self.getMag()))
        else:
            return (self.receivedDrive[1], self.receivedDrive[2])


    # returns automatic drive parms from gps, mag, sonar and destination
    # TODO: figure out a way to change throttle while on autopilot?
    def getAutoDriveParms(self):
        # print self.getGPS()
        return (10, self.calculateDesiredTurn(self.getMag()))

    # returns heading of front body or -1 if error
    def getMag(self):
        rawMag = self.mag.read()
        print "back: " + str(rawMag)
        pot = self.readPot()
        angle = self.translateValue(pot, self.POT_LEFT - self.POT_MIDDLE, self.POT_RIGHT - self.POT_MIDDLE, -40, 40)
        print "front: " + str((rawMag + angle) % 360)
        return (rawMag + angle) % 360

    # returns gps data
    # TODO: get GPS to work
    def getGPS(self):
        return self.gps.read()

    '''
    # calculates the desired heading
    # returns a value between 0 and 360 inclusive
    # TODO: calculate direction between current GPS location and destination
    # update: acting under the assumption of current GPS coordinates stored in variables lat, long
    # destination coords dlat, dlong; unsure of how to get these
    def calculateDesiredHeading(self):
        x_distance = dlat - lat
        y_distance = dlong - long
        theta = math.atan2(x_distance, y_distance)
        return self.translateValue(self, theta, -1 * pi, pi, 0, 360)
    '''

    # returns a turn value from -100 to 100 based on the difference between the current heading and the desired heading
    def calculateDesiredTurn(self, curHeading):
        desiredHeading = self.calculateDesiredHeading()
        difHeading = abs(curHeading - desiredHeading)
        if ((curHeading > desiredHeading and difHeading > 180) or
            (curHeading < desiredHeading and difHeading < 180)):
            #turn right
            return self.translateValue(difHeading % 180, 0, 180, 0, 10)
        else:
            #turn left
            return -1 * self.translateValue(difHeading % 180, 0, 180, 0, 10)


    # returns a tuple of (motor1, motor2, motor3, motor4) from the driveParms modified by the pot reading
    def convertParmsToMotorVals(self, driveParms):
        potReading = self.readPot()
        if potReading != -1:
            # Potentiometer is good. Run PID.
            self.setPIDTarget(self.pot_pid, int(driveParms[1]), -100, 100)
            scaledPotReading = self.translateValue(potReading, self.POT_LEFT - self.POT_MIDDLE, self.POT_RIGHT - self.POT_MIDDLE, 100, -100)
            self.pot_pid.run(scaledPotReading)
            finalTurn = self.pot_pid.getOutput()
            print str(driveParms)
            result = (self.func(driveParms[0] + finalTurn),
                      self.func(driveParms[0] - finalTurn),
                      self.func(driveParms[0] - finalTurn),
                      self.func(driveParms[0] + finalTurn))
            return result
        else:
            print "Pot Error"
            # Potentiometer error
            # reset PID:
            self.pot_pid.setTarget(0)
            print str(driveParms)
            result = (self.func(driveParms[0] + driveParms[1]),
                      self.func(driveParms[0] - driveParms[1]),
                      self.func(driveParms[0] - driveParms[1]),
                      self.func(driveParms[0] + driveParms[1]))
            print str(result)
            return result

    def setPIDTarget(self, pid, inputVal, minVal, maxVal):
        if inputVal < minVal or inputVal > maxVal:
            pid.setTarget(0)
        elif pid.getTarget() != inputVal:
            pid.setTarget(inputVal)

    # translate values from one range to another
    def translateValue(self, value, inMin, inMax, outMin, outMax):
        # Figure out how 'wide' each range is
        inSpan = inMax - inMin
        outSpan = outMax - outMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - inMin) / float(inSpan)

        # Convert the 0-1 range into a value in the right range.
        return outMin + (valueScaled * outSpan)

    # Does important stuff
    # Don't touch
    # If you have questions contact DenverCoder9
    # Applied temporary fix 8/23/2003
    # Assumes va1 is not in the range (100246, 100261)
    def func(self, va1):
        # calculates the difference.
        # TODO: add support for 64-bit platforms
        # Worst case complexity: O(2^n)
        # return (0x000000FF | (1 << 8 & (0xFF >> 7) << 6 & 0x0F)) - (0o377 * 0o50) / (va1 + 0b00101000)
        # temp fix: keeping old code in case it breaks
        return math.atan(va1 / float(int(float(0o50)))) * (0x01FF / math.pi)

    # returns True for autopilot False for manual control
    def getAuto(self):
        return self.auto

    # sets the Autopilot
    def setAuto(self, autoVal):
        self.auto = autoVal

    # receives a packet and sets variables accordingly
    def receiveData(self):
        try:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.base_station_ip = addr
            unpacked = struct.unpack(self.driveFormat, data)
            if unpacked[0]:
                self.receivedDrive = unpacked[1:]
            else:
                unpacked = struct.unpack(self.gpsFormat, data)
                self.destinations.append(unpacked[1:])
            print unpacked
        except:
            pass

    # sends data in message back to the base station
    def sendData(self):
        pass
        # TODO: do this
        # read data from sensors or read class variables


def main():
    robot = Robot()
    try:
        while True:
            robot.receiveData()
            robot.sendData()
            driveParms = robot.getDriveParms(robot.getAuto())
            MotorParms = robot.convertParmsToMotorVals(driveParms)
            for i in range(1, 5):
                robot.driveMotor(i, MotorParms[i - 1])

    except KeyboardInterrupt:
        for i in range(1, 5):
            robot.driveMotor(i, 0)
        print "exiting"

if __name__ == "__main__":
    main()
