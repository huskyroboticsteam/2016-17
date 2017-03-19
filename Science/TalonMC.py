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
import Adafruit_GPIO.PWM as PWM


class TalonMC:

    _freq = 4000  # from the Talon spec

    def __init__(self, pin):
        self._pin = pin
        self._motor = PWM.BBIO_PWM_Adapter(PWM.get_platform_pwm())
        self._motor.set_frequency(self._pin, self._freq)

    def enable(self):
        self._motor.start(self._pin, 0.0, self._freq)

    def set(self, value):
        self._motor.set_duty_cycle(self._pin, value)

    def stop(self):
        self._motor.stop(self._pin)

    def setFreq(self, freq): # do not call while motor running
        self._freq = freq
        self._motor.set_frequency(self._pin, self._freq)
        self.enable()
