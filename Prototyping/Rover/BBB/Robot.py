import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import time
import PID
import math
import MiniMotor
import BigMotor
import socket
import struct
import Navigation
import Utils

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

        self.pot_pid = PID.PID(-0.1, 0, 0)

        self.nav = Navigation.Navigation(0.771, 0.346, (0.771 + 0.346) / 2, 0.01, "AIN2")
        # setup motors
        # motor: throttle, F, B
        # 1: 8,  9,  10
        # 2: 13, 12, 11
        # 3: 2,  4,  3
        # 4: 7,  6,  5
        self.motors = [
            None, # motor IDs are 1-based, so placeholder for index 0
            MiniMotor.MiniMotor(1, 8, 9, 10, self.pwm),
            MiniMotor.MiniMotor(2, 13, 12, 11, self.pwm),
            MiniMotor.MiniMotor(3, 2, 4, 3, self.pwm),
            MiniMotor.MiniMotor(4, 7, 6, 5, self.pwm),
        ]
        self.receivedDrive = None
        self.robot_ip = "192.168.0.40"
        self.udp_port = 8840
        self.base_station_ip = None
        self.driveFormat = "<??hh"
        self.gpsFormat = "<?hhhhhh"
        self.rtbFormat = "<fffffhhhhhh"
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.robot_ip, self.udp_port))
        self.sock.setblocking(False)

    # drives the motor with a value, negative numbers for reverse
    def driveMotor(self, motor_id, motor_val):
        if motor_id < 1 or motor_id > 4:
            print "bad motor num: " + motor_id
            return
        self.motors[motor_id].set_motor(motor_val)

    # returns a 2-tuple of (throttle, turn)
    # turn value is 100 for full right -100 for full left and 0 for straight
    def getDriveParms(self, auto):
        if self.receivedDrive == None:
            return 0, 0
        auto = self.receivedDrive[0]
        if auto:
            return 20, self.nav.calculateDesiredTurn(self.nav.getMag())
        else:
            return self.receivedDrive[1], self.receivedDrive[2]

    # returns automatic drive parms from gps, mag, sonar and destination
    # TODO: figure out a way to change throttle while on autopilot?
    def getAutoDriveParms(self):
        # print self.getGPS()
        return 10, self.nav.calculateDesiredTurn(self.nav.getMag())

    # returns a tuple of (motor1, motor2, motor3, motor4) from the driveParms modified by the pot reading
    def convertParmsToMotorVals(self, driveParms):
        potReading = self.nav.readPot()
        if potReading != -1:
            # Potentiometer is good. Run PID.
            self.setPIDTarget(self.pot_pid, int(driveParms[1]), -100, 100)
            scaledPotReading = Utils.translateValue(potReading, self.nav.get_pot_left() - self.nav.get_pot_middle(), \
                                                    self.nav.get_pot_right() - self.nav.get_pot_middle(), 100, -100)
            self.pot_pid.run(scaledPotReading)
            finalTurn = self.pot_pid.getOutput()
            print str(driveParms)
            result = (self.scale_motor_val(driveParms[0] + finalTurn),
                      self.scale_motor_val(driveParms[0] - finalTurn),
                      self.scale_motor_val(driveParms[0] - finalTurn),
                      self.scale_motor_val(driveParms[0] + finalTurn))
            return result
        else:
            print "Pot Error"
            # Potentiometer error
            # reset PID:
            self.pot_pid.setTarget(0)
            print str(driveParms)
            result = (self.scale_motor_val(driveParms[0] + driveParms[1]),
                      self.scale_motor_val(driveParms[0] - driveParms[1]),
                      self.scale_motor_val(driveParms[0] - driveParms[1]),
                      self.scale_motor_val(driveParms[0] + driveParms[1]))
            print str(result)
            return result

    def setPIDTarget(self, pid, inputVal, minVal, maxVal):
        if inputVal < minVal or inputVal > maxVal:
            pid.setTarget(0)
        elif pid.getTarget() != inputVal:
            pid.setTarget(inputVal)



    # a monotonically increasing function with output of -256 < x < 256
    # scales the motor value for driving the motors so that it never has a value outside of the safe range
    def scale_motor_val(self, val):
        return math.atan(val / 40) * (255 * 2 / math.pi)


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
                self.nav.append_destination(unpacked[1:])
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
