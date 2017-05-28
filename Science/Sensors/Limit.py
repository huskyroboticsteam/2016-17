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

    event_found = False

    # Sets pin of limit switch
    def __init__(self, pin):
        global LIMITS
        self._limitPin = str(pin)
        try:
            GPIO.setup(self._limitPin, GPIO.IN)
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
            val = int(GPIO.input(self._limitPin)) == 1  # Ensures boolean
        except:
            # Throw "Could not read DIO Pin"
            Error.throw(0x0003)
        return val

    # Returns data for packet
    def getDataForPacket(self):
        return Util.long_to_byte_length(int(self.getValue()), 1)

    def waitForSwitchChange(self, timeout=300):
        GPIO.remove_event_detect(self._limitPin)
        GPIO.add_event_detect(self._limitPin, GPIO.BOTH)
        start_time = time.time()
        while not GPIO.event_detected(self._limitPin) and (time.time() - start_time) < timeout:
            pass

    @classmethod
    def getAllData(cls):
        global LIMITS
        data = 0
        for i in range(0, len(LIMITS)):
            data |= int(LIMITS[i].getValue()) << i
        return Util.long_to_byte_length(data, 1)
