"""
Reads a Digital IO on the Beaglebone Black
to determine the on/off characteristic of a
limit switch.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import sys
sys.path.insert(0, '../')
import Util
import Error
import Adafruit_BBIO.GPIO as GPIO  # Ignore compiler errors
from Sensor import Sensor


class Limit(Sensor):

    # Sets pin of limit switch
    def __init__(self, pin):
        self._pin = str(pin)
        try:
            GPIO.setup(self._pin, GPIO.IN)
        except:
            # Throw "Could not setup DIO Pin"
            self.critical_status = True
            Error.throw(0x0002)

    # Returns on/off (boolean) characteristic of the pin
    # at any given time
    def getValue(self):
        if self.critical_status:
            return 0
        val = 0
        try:
            val = GPIO.input(self._pin)
        except:
            # Throw "Could not read DIO Pin"
            Error.throw(0x0003)
        return val

    # Returns data for packet
    def getDataForPacket(self):
        return Util.long_to_byte_length(int(self.getValue()), 1)

