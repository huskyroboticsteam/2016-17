"""
Reads a Digital IO on the Beaglebone Black
to determine the on/off characteristic of a
limit switch.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import Util
import Error
import time
import Adafruit_BBIO.GPIO as GPIO  # Ignore compiler errors
from Sensor import Sensor
from threading import Thread

LIMITS = []

class Limit(Sensor):

    # Sets pin of limit switch
    def __init__(self, pin):
        global LIMITS
        self._pin = str(pin)
        try:
            GPIO.setup(self._pin, GPIO.IN)
        except:
            # Throw "Could not setup DIO Pin"
            self.critical_status = True
            Error.throw(0x0002)
        LIMITS += [self]
        

    # Returns on/off (boolean) characteristic of the pin
    # at any given time
    def getValue(self):
        val = False
        if self.critical_status:
            return val
        try:
            val = GPIO.input(self._pin)
        except:
            # Throw "Could not read DIO Pin"
            Error.throw(0x0003)
        return val

    # Returns data for packet
    def getDataForPacket(self):
        return Util.long_to_byte_length(int(self.getValue()), 1)

    def waitForSwitchChange(self, timeout=300):
        waitingFor = not self.getValue()
        def wait():
            if self.getValue():
                GPIO.wait_for_edge(self._pin, GPIO.RISING)
            else:
                GPIO.wait_for_edge(self._pin, GPIO.FALLING)
        thread = Thread(target=wait)
        thread.start()
        thread.join(timeout)

    @classmethod
    def getAllData(cls):
        global LIMITS
        data = 0
        for i in range(0, len(LIMITS)):
            data |= int(LIMITS[i].getValue()) << i
        return Util.long_to_byte_length(data, 1)

