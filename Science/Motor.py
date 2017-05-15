import Adafruit_GPIO.PWM as PWM
import time
import Util

"""

"""


class Motor:

    pwm_handler = PWM.get_platform_pwm()
    pwm_working = ["P9_14", "P9_16", "P9_42", "P9_21", "P8_13", "P8_19"]
    motors = []
    _freq = 2000
    _started = False

    def __init__(self, pin):
        self._pin = pin
        self.pwm_handler.start(self._pin, 0.0)
        self._started = True
        self.motors += [self]

    def enable(self):
        pass

    def set(self, value):
        self.pwm_handler.set_duty_cycle(self._pin, ((value % 100) * 100.0))

    def stop(self):
        self.pwm_handler.stop(self._pin)

    def calibrate(self):
        pass

    def setFreq(self, freq):
        self.pwm_handler.set_frequency(self._pin, freq)
        self._freq = freq

    @classmethod
    def getMotors(cls):
        return cls.motors

    @classmethod
    def enableAll(cls):
        for motor in cls.motors:
            motor.enable()

    @classmethod
    def stopAll(cls):
        for motor in cls.motors:
            motor.stop()
            cls.pwm_handler.stop(motor._pin)
        cls.pwm_handler.cleanup()

    @classmethod
    def initializeAllPWMPins(cls):
        for pin in cls.pwm_working:
            cls.pwm_handler.stop(pin)
        

    @classmethod
    def calibrateAll(cls):
        for motor in cls.motors:
            motor.calibrate()

    def isStarted(self):
        return self._started

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

    _freq = 4000  # from the Talon spec

    def __init__(self, pin):
        Motor.__init__(self, pin)
        self._calibration = TalonCalibration(self._pin)

    def calibrate(self):
        self._calibration.calibrate()


"""

"""


class Servo(Motor):

    _minDutyCycle = 3.0
    _maxDutyCycle = 14.5

    def __init__(self, pin):
        Motor.__init__(self, pin)

    def setMinDutyCycle(self, minDutyCycle):
        self._minDutyCycle = minDutyCycle

    def setMaxDutyCycle(self, maxDutyCycle):
        self._maxDutyCycle = maxDutyCycle

    def moveTo(self, angle):
        dutyCycle = 100 - ((angle / 180.0) * (self._maxDutyCycle - self._minDutyCycle) + self._minDutyCycle)
        self.pwm_handler.set_duty_cycle(self._pin, dutyCycle)


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
        while time.time() - start_time < 0.5:
            self._motor.set(1.0)
        start_time = time.time()
        while time.time() - start_time < 0.5:
            self._motor.set(0.0)
