import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import PID
import math
import Servo_Sweep
import Sonar
import threading
import MiniMotor
import BigMotor
import Robot_comms
import Navigation
import Utils
import sys
import time
from autonomous import Autonomous
from random import random
from Utils import scale_coords
import Adafruit_BBIO.PWM as PWM
import basicAutonomous

class RobotTest(object):
    """
    Class for controlling the whole robot.

    Attributes:
        pot_pid (PID.PID): PID controller for the potentiometer.
        nav (Navigation.Navigation): Object for managing navigation.
        motors (list of Motor.Motor): The list (of length 4, 0-based) of motors.
        r_comms (Robot_comms.Robot_comms): Object for managing communicationg
            with the base station.
        autonomous_initialized (bool): True iff we initialized and set target for the autonomous mode.
        autonomous (Autonomous): Object for managing autonomous navigation (and path finding).

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
    """

    def __init__(self, is_using_big_motor):
        """
        Args:
            is_using_big_motor (bool): True if using BigMotor for controller motors.
        """
        ADC.setup()

        # setup motors
        # motor: throttle, F, B
        # 1: 8,  9,  10
        # 2: 13, 12, 11
        # 3: 2,  4,  3
        # 4: 7,  6,  5

        if is_using_big_motor == "0":
            # setup i2c to motorshield
            pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
            pwm.set_pwm_freq(60)
            self.pot_pid = PID.PID(-0.1, 0, 0) #TODO Adjust
            self.nav = Navigation.Navigation(0.765555, 0.552777, 0.348333, 0.001, "AIN2")
            self.r_comms = Robot_comms.Robot_comms("192.168.0.40", 8840, 8841, "<?hh", "<?ff", "<ffffffff", "<?ff?", self.nav)
            self.motors = [
                MiniMotor.MiniMotor(1, 8, 9, 10, pwm),
                MiniMotor.MiniMotor(2, 13, 12, 11, pwm),
                MiniMotor.MiniMotor(3, 2, 4, 3, pwm),
                MiniMotor.MiniMotor(4, 7, 6, 5, pwm),
            ]
        else:
            self.pot_pid = PID.PID(-.7, -0.8, 0)
            self.nav = Navigation.Navigation(0.60, 0.3166666, 0.14, 0.001, "AIN2")
            self.r_comms = Robot_comms.Robot_comms("192.168.0.50", 8840, 8841, "<?hh", "<?ff", "<ffffffff", "<?ff?", self.nav)
            self.motors = [
                BigMotor.BigMotor(1, "P9_21"),
                BigMotor.BigMotor(2, "P9_16"),
                BigMotor.BigMotor(3, "P9_14"),
                BigMotor.BigMotor(4, "P9_22")
                ]
            servo_pin_1 = "P9_14"
            servo_pin_2 = "P9_22"
            servo_pin_3 = "P9_16"
            servo_pin_4 = "P9_21"
            PWM.start(servo_pin_1, 1.5/17.6, 60)
            PWM.start(servo_pin_2, 1.5/17.6, 60)
            PWM.start(servo_pin_3, 1.5/17.6, 60)
            PWM.start(servo_pin_4, 1.5/17.6, 60)
            PWM.set_duty_cycle(servo_pin_1, 1.5 * 100/17.6)
            PWM.set_duty_cycle(servo_pin_2, 1.5 * 100/17.6)
            PWM.set_duty_cycle(servo_pin_3, 1.5 * 100/17.6)
            PWM.set_duty_cycle(servo_pin_4, 1.5 * 100/17.6)

        self.autonomous_initialized = False
        self.autonomous = Autonomous()
        self.Sweeper = Servo_Sweep.Servo_Sweep(0.005, 1, 179, "P8_13")
        self.sonar = Sonar.Sonar()
        self.target = None

        # Used to keep track of number of obstacles seem in a row
        self.obsCount = 0

    def moveServo(self):
        self.Sweeper.move()

    def driveMotor(self, motor_id, motor_val):
        """
        Drive one motor.

        Args:
            motor_id (int): The 1-based ID of the motor to drive
            motor_val (int): How much power to drive the motor. Use negative
                numbers to drive in reverse.
        """
        if motor_id < 1 or motor_id > 4:
            print "bad motor num: " + motor_id
            return
        self.motors[motor_id - 1].set_motor(motor_val)

    def stopMotor(self, motor_id):
        """
        Stop one motor.

        Args:
            motor_id (int): The 1-based ID of the motor to stop
        """
        if motor_id < 1 or motor_id > 4:
            print "bad motor num: " + motor_id
            return
        self.motors[motor_id - 1].set_motor_exactly(0)

    def getDriveParms(self):
        """
        Gets the driving parameters of the rover.

        Returns:
            tuple of (int, int): The drive parameters in the format (throttle, turn).
                For the turn value, 100 is full right, -100 is full left, and 0
                is straight.
        """
        # if self.r_comms.receivedDrive is None:
        #     return 0, 0
        # auto = self.r_comms.receivedDrive[0]
        if True:
            time.sleep(.4)
            location = self.nav.getGPS()
            if location is None:
                location = (0, 0)
            if not self.autonomous_initialized:
                # TODO: read target from wireless
                self.target = (47.6530883, -122.30722)
                self.autonomous.set_target(self.target)
                self.autonomous_initialized = True
            if self.autonomous.is_done(location):
                # Reached the target
                # sends back "we're here" signal
                print "arrived at desired location"
                self.r_comms.sendAtLocationPacket(self.nav)
                return 0, 0
            else:
                heading = self.nav.getMag()
                #print "heading: ", heading
                #print "location: ", location
                #print "desired location: ", self.target
                if location == (0.0, 0.0) or location == (0, 0):
                    print "gps not received, staying still"
                    return 0, 0
                # if self.sonar.readDisM() < self.sonar.getMaxDisM(): # Make sure obstacle is greater than infinity value
                #     if self.obsCount < 5: # Filters out random garbage values if there even is any
                #         self.obsCount+= 1
                #     else: # Add obstacle to autonomous
                #         self.autonomous.add_obstacle(Utils.point_at_end(location, Utils.normalize_angle(90 - self.Sweeper.currentAngle), self.sonar.readDisM()))
                # else: # Sets the obs count to zero saying there hasn't been a obstacle
                #     self.obsCount = 0
                turn = self.autonomous.go(location, heading)
                print "turn: ", turn
                # Smoother turns at low turn, otherwise max turn
                if abs(turn) < 20:
                    return 100, turn * 3
                elif turn > 0:
                    return 100, 100
                else:
                    return 100, -100

        else:
            return self.r_comms.receivedDrive[1], self.r_comms.receivedDrive[2]

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
            #print str(driveParms)
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
            #print str(driveParms)
            result = (self.scale_motor_val(driveParms[0] + driveParms[1]),
                      self.scale_motor_val(driveParms[0] - driveParms[1]),
                      self.scale_motor_val(driveParms[0] - driveParms[1]),
                      self.scale_motor_val(driveParms[0] + driveParms[1]))
            #print str(result)
            return result

    @staticmethod
    def setPIDTarget(pid, inputVal, minVal, maxVal):
        if inputVal < minVal or inputVal > maxVal:
            pid.setTarget(0)
        elif pid.getTarget() != inputVal:
            pid.setTarget(inputVal)

    # a monotonically increasing function with output of -256 < x < 256
    # scales the motor value for driving the motors so that it never has a value outside of the safe range
    @staticmethod
    def scale_motor_val(val):
        return math.atan(val / 40) * (255 * 2 / math.pi)

    def get_robot_comms(self):
        return self.r_comms

    def get_nav(self):
        return self.nav


class DriveParams:
    """
    Object to hold drive parameters, so that only one thread can access it
    at a time.

    Attributes:
        throttle, turn (float): The current drive parameters
        is_stopped (bool): Whether the robot should be stopped.
        lock (threading.Lock): The lock that protects the data.
    """
    def __init__(self):
        self.throttle = 0.0
        self.turn = 0.0
        self.is_stopped = False
        self.lock = threading.Lock()

    def set(self, throttle, turn):
        """
        Args:
            throttle, turn (float)
        """
        with self.lock:
            self.throttle = float(throttle)
            self.turn = float(turn)

    def stop(self):
        """
        Use this method when you want to stop the robot.
        """
        with self.lock:
            self.is_stopped = True

    def get(self):
        """
        Returns:
            either tuple of (float, float) or None: The throttle and turn, or
                None if the robot should be stopped.
        """
        with self.lock:
            if self.is_stopped:
                temp = None
            else:
                temp = self.throttle, self.turn
        return temp


class DriveThread(threading.Thread):
    """
    Thread that continuously reads the throttle and turn from a DriveParams
    object and makes the robot move accordingly.

    Attributes:
        robot (Robot): Object for controlling the robot.
        drive_params (DriveParams): Read the throttle and turn from this object.
    """
    def __init__(self, drive_params, is_using_big_motor):
        super(DriveThread, self).__init__()
        self.robot = RobotTest(is_using_big_motor)
        self.drive_params = drive_params

    def run(self):
        """
        Overrides a method in threading.Thread. Do not call this method
        directly; use start() instead.
        """
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
        drive_thread = DriveThread(drive_params, sys.argv[1])
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
        robot = RobotTest(sys.argv[1])
        try:
            while True:
                robot.moveServo()
                robot.get_robot_comms().receiveData(robot.get_nav())
                robot.get_robot_comms().sendData(robot.get_nav())
                driveParms = robot.getDriveParms()
                MotorParms = robot.convertParmsToMotorVals(driveParms)
                print "motor parms: ", MotorParms
                for i in range(1, 5):
                    robot.driveMotor(i, MotorParms[i - 1])

        except KeyboardInterrupt:
            for i in range(1, 5):
                try:
                    robot.stopMotor(i)
                except:
                    print("motor: " + str(i) + " disconnected")
            PWM.cleanup()
            robot.r_comms.closeConn()
            print "exiting"

if __name__ == "__main__":
    main()
