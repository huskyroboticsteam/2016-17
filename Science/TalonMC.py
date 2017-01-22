import Adafruit_GPIO.PWM as PWM


class TalonMC(object):

    _freq = 15625 # from the Talon spec

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