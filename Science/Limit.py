"""
Reads a Digital IO on the Beaglebone Black
to determine the on/off characteristic of a
limit switch.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
(Untested as of 2/6/2017)
"""


class Limit:

    # Sets pin of limit switch
    def __init__(self, pin, gpio):
        self._pin = pin
        self._gpio = gpio

    # Returns on/off (boolean) characteristic of the pin
    # at any given time
    def status(self):
        return self._gpio.is_high(self._pin)
