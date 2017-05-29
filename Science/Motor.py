import Adafruit_BBIO.PWM as PWM
import time
import Util

"""

"""


class Motor:

    pwm_working = ["P9_14", "P9_16", "P9_42", "P9_21", "P8_13", "P8_19"]
    motors = []

    def __init__(self, pin, freq=50):
        self._pin = pin
        PWM.start(self._pin, 0.0, freq)
        Motor.motors += [self]

    def enable(self):
        pass

    """
    Input float % 0 to 1 inclusive
    """
    def set(self, value):
        PWM.set_duty_cycle(self._pin, ((value % 1) * 100.0))

    def stop(self):
        PWM.stop(self._pin)

    def calibrate(self):
        pass

    @classmethod
    def getMotors(cls):
        return Motor.motors

    @classmethod
    def enableAll(cls):
        for motor in Motor.motors:
            motor.enable()

    @classmethod
    def stopAll(cls):
        for motor in Motor.motors:
            motor.stop()
            PWM.stop(motor._pin)
        PWM.cleanup()

    @classmethod
    def initializeAllPWMPins(cls):
        PWM.cleanup()
        

    @classmethod
    def calibrateAll(cls):
        for motor in Motor.motors:
            motor.calibrate()


"""
Interfaces Beaglebone Black PWM outputs with
a Talon Motor Controller.

More research needs to go into the operation of a
Talon Motor Controller before this code
is tested with an actual motor.
Refer to author with questions.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

Talon Spec
https://content.vexrobotics.com/vexpro/pdf/Talon-SRX-User-Guide-20150201.pdf
Page 29 has PWM Calibration information

"""


class TalonMC(Motor):


    def __init__(self, pin):
        Motor.__init__(self, pin, 333)
        self._calibration = TalonCalibration(self)

    def calibrate(self):
        self._calibration.calibrate()

    # -1 to 1 % power
    def set(self, percent_power):
        output = Util.map(percent_power, -1.0, 1.0, 1.0, 99.0)
        PWM.set_duty_cycle(self._pin, output % 100.0)



"""

"""


class Servo(Motor):

    _minDutyCycle = 1.0
    _maxDutyCycle = 4.0

    def __init__(self, pin):
        Motor.__init__(self, pin)

    def setMinDutyCycle(self, minDutyCycle):
        self._minDutyCycle = minDutyCycle

    def setMaxDutyCycle(self, maxDutyCycle):
        self._maxDutyCycle = maxDutyCycle

    def moveTo(self, angle):
        dutyCycle = 100 - ((angle / 180.0) * (self._maxDutyCycle - self._minDutyCycle) + self._minDutyCycle)
        self.set(dutyCycle / 100.0)


"""
This class is meant to be used to calibrate a Talon
Motor Controller.

Documentation on calibration here:
https://content.vexrobotics.com/vexpro/pdf/Talon-SRX-Users-Guide-20170226.pdf
Page 29 has PWM Calibration information

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Tested as of 2/25/2017)

"""


class TalonCalibration:

    def __init__(self, motor):
        self._motor = motor

    def calibrate(self):
        start_time = time.time()
        while time.time() - start_time < 5:
            self._motor.set(1.0)
        start_time = time.time()
        while time.time() - start_time < 5:
            self._motor.set(-1.0)
        self._motor.set(0.0)
