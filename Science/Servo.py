"""


"""

import Adafruit_GPIO.PWM as PWM


class Servo:

    def __init__(self, pin):
        self._motor = PWM.BBIO_PWM_Adapter(PWM.get_platform_pwm())
        self._pin = pin