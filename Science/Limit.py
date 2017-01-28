import Adafruit_GPIO.GPIO as GPIO


class Limit(object):

    def __init__(self, pin):
        self._pin = pin

    def status(self):
        return GPIO.BaseGPIO.is_high(self._pin)
