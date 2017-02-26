import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import PID
import math
import threading
import MiniMotor
import BigMotor
import Robot_comms
import Navigation
import Utils
import time
import sys
import getopt

class Robot(object):
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

    def __init__(self, arg):
        ADC.setup()


        self.pot_pid = PID.PID(-0.1, 0, 0)

        self.nav = Navigation.Navigation(0.55000, (0.55000 + 0.11111) / 2, 0.11111, 0.01, "AIN2")
        # setup motors
        # motor: throttle, F, B
        # 1: 8,  9,  10
        # 2: 13, 12, 11
        # 3: 2,  4,  3
        # 4: 7,  6,  5


        if not arg:
            # setup i2c to motorshield
            self.pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
            self.pwm.set_pwm_freq(60)
            self.motors = [

                None, # motor IDs are 1-based, so placeholder for index 0
                MiniMotor.MiniMotor(1, 8, 9, 10, self.pwm),
                MiniMotor.MiniMotor(2, 13, 12, 11, self.pwm),
                MiniMotor.MiniMotor(3, 2, 4, 3, self.pwm),
                MiniMotor.MiniMotor(4, 7, 6, 5, self.pwm),
            ]
        elif arg:
            self.motors = [
                BigMotor.BigMotor(1, "P8_13"),
                BigMotor.BigMotor(2, "P8_19"),
                BigMotor.BigMotor(3, "P9_14"),
                BigMotor.BigMotor(4, "P8_13")
                ]
        self.r_comms = Robot_comms.Robot_comms("192.168.0.50", 8840, 8841, "<?hh", "<?ff", "<ffffffff")
        self.automode = 0

    # drives the motor with a value, negative numbers for reverse
    def driveMotor(self, motor_id, motor_val):
        if motor_id < 1 or motor_id > 4:
            print "bad motor num: " + motor_id
            return
        self.motors[motor_id - 1].set_motor(motor_val)

    def stopMotor(self, motor_id):
        if motor_id < 1 or motor_id > 4:
            print "bad motor num: " + motor_id
            return
        self.motors[motor_id].set_motor_exactly(0)

    # returns a 2-tuple of (throttle, turn)
    # turn value is 100 for full right -100 for full left and 0 for straight
    def getDriveParms(self, auto):
        if self.r_comms.receivedDrive == None:
            return 0, 0
        auto = self.r_comms.receivedDrive[0]
        if auto:
            if self.automode == 0:  # Auto drive normaly
                if self.nav.isObstacle(): # if obstacle in front then switch mode
                    self.automode = 1
                else:
                    return 20, self.nav.calculateDesiredTurn(self.nav.getMag(), self.nav.calculateDesiredHeading())
            if self.automode == 1:  # Turn rover head to left to prepare to scan
                if self.nav.readPot() < self.nav.get_pot_left():
                    leftheading = (self.nav.getMag() - 40) % 360
                    if (leftheading < 0):
                        leftheading = 360 - leftheading
                    return 0, self.nav.calculateDesiredTurn(self.nav.getMag(), leftheading)
                else:
                    self.automode = 2
            if self.automode == 2:  # Scan in front of rover at an arch from left to right recording values
                if self.nav.readPot() > self.nav.get_pot_right():
                    self.nav.appendScannedHeadings()
                    rightheading = (self.nav.getMag() + 40) % 360
                    return 0, self.nav.calculateDesiredTurn(self.nav.getMag(), rightheading)
                else:
                    self.nav.addDestination()  # Get a new heading and add a temp value to coordinate list
                    self.automode = 0 # start driving in auto normally
        else:
            return self.r_comms.receivedDrive[1], self.r_comms.receivedDrive[2]

    # returns automatic drive parms from gps, mag, sonar and destination
    # TODO: figure out a way to change throttle while on autopilot?
    def getAutoDriveParms(self):
        # print self.getGPS()
        return 10, self.nav.calculateDesiredTurn(self.nav.getMag(), self.nav.calculateDesiredHeading())

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

    def get_robot_comms(self):
        return self.r_comms

    def get_nav(self):
        return self.nav


class DriveParams:
    def __init__(self):
        self.throttle = 0.0
        self.turn = 0.0
        self.is_stopped = False
        self.lock = threading.Lock()

    def set(self, throttle, turn):
        with self.lock:
            self.throttle = throttle
            self.turn = turn

    def stop(self):
        with self.lock:
            self.is_stopped = True

    def get(self):
        temp = ()
        with self.lock:
            if self.is_stopped:
                temp = None
            else:
                temp = self.throttle, self.turn
        return temp


class DriveThread(threading.Thread):
    def __init__(self, drive_params):
        super(DriveThread, self).__init__()
        self.robot = Robot()
        self.drive_params = drive_params

    def run(self):
        while True:
            drive_params = self.drive_params.get()
            if drive_params is None:
                break
            motor_params = self.robot.convertParmsToMotorVals(drive_params)
            for i in range(1, 5):
                self.robot.driveMotor(i, motor_params[i - 1])
        for i in range(1, 5):
            self.robot.stopMotor(i)


def main():
    choice = raw_input('Control robot with keyboard? (y/n) ')
    if choice[0] == 'y':
        drive_params = DriveParams()
        drive_thread = DriveThread(drive_params)
        drive_thread.start()
        print 'Enter throttle followed by turn, separated by spaces.'
        print 'For turn, 100 is full right, -100 is full left.'
        try:
            while True:
                in_str = raw_input('input: ')
                in_list = in_str.split()
                throttle = float(in_list[0])
                turn = float(in_list[1])
                drive_params.set(throttle, turn)
        except KeyboardInterrupt:
            drive_params.stop()
            drive_thread.join()
    else:
        robot = Robot(sys.argv[1])
        try:
            while True:
                robot.get_robot_comms().receiveData(robot.get_nav())
                #robot.get_robot_comms().sendData(robot.get_nav())
                driveParms = robot.getDriveParms(robot.get_nav().getAuto())
                MotorParms = robot.convertParmsToMotorVals(driveParms)
                for i in range(1, 5):
                    robot.driveMotor(i, MotorParms[i - 1])

        except KeyboardInterrupt:
            for i in range(1, 5):
                try:
                    robot.stopMotor(i)
                except:
                    print("motor: " + str(i) + " disconnected")
            robot.r_comms.closeConn()
            print "exiting"

if __name__ == "__main__":
    main()
