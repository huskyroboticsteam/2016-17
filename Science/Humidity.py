"""
Reads an Analog Humidity Sensor on an Analog Pin
on the Beaglebone Black

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Tested as of 2/25/2017)

NOTE: ADC Must Be Initialized Prior to Initialization / Construction of
this sensor.

NOTE: Beaglebone Black ADC has a 12-bit resolution

"""

import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Sensor import Sensor
import Util


class Humidity(Sensor):

    # Initializes the Humidity Sensor on given pin
    def __init__(self, pin):
        self._pin = "AIN" + str(pin)  # Pin for the sensor
        self._m = 1  # Calibration intercept
        self._int = 0  # Calibration slope

    # Reads raw ADC value
    def readRaw(self):
        # Reading twice per the Adafruit Documentation,
        # which warns of a bug if you neglect to read
        # twice
        ADC.read(self._pin)
        return ADC.read(self._pin)

    # Reads calibrated raw values
    def getValue(self):
        return self._m * self.readRaw() + self._int

    # Sets linear calibration constants for read()
    # slope = slope of linear calibration;
    # i = intercept of linear calibration.
    def setup(self, slope, i):
        self._m = slope
        self._int = i

    def getDataForPacket(self):
        return Util.inttobin(self.readRaw(), 16)
