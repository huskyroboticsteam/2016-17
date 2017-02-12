"""
Reads an Analog Humidity Sensor on an Analog Pin
on the Beaglebone Black

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
(Untested as of 2/6/2017)

NOTE: ADC Must Be Initialized Prior to Initialization / Construction of
this sensor.
NOTE: Beaglebone Black ADC has a 12-bit resolution
"""

import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors


class Humidity:

    # Initializes the Humidity Sensor on given pin
    def __init__(self, pin):
        self._pin = "AIN" + pin  # Pin for the sensor
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
    def read(self):
        return self._m * self.readRaw() + self._int

    # Sets linear calibration constants for read()
    # slope = slope of linear calibration;
    # i = intercept of linear calibration.
    def setup(self, slope, i):
        self._m = slope
        self._int = i
