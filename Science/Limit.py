"""
Reads a Digital IO on the Beaglebone Black
to determine the on/off characteristic of a
limit switch.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
(Untested as of 2/6/2017)
"""
import Adafruit_BBIO.GPIO as GPIO  # Ignore compiler errors


class Limit:

    # Sets pin of limit switch
    def __init__(self, pin):
        self._pin = pin
        GPIO.setup(self._pin, GPIO.IN)

    # Returns on/off (boolean) characteristic of the pin
    # at any given time
    def status(self):
        return GPIO.input(self._pin)
