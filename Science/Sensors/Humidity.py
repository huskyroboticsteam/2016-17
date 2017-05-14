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
import sys
sys.path.insert(0, '../')
import Util
import Error
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Sensor import Sensor


class Humidity(Sensor):

    _m = 1
    _int = 0

    # Initializes the Humidity Sensor on given pin
    def __init__(self, pin):
        self._pin = str(pin)  # Pin for the sensor
        self._m = 1  # Calibration intercept
        self._int = 0  # Calibration slope

        # Setup the ADC if not already done
        if not Util.ADC_Status():
            try:
                ADC.setup()
                Util.setADC_Status(True)
            except:
                # Throw "Communication Failure"
                Error.throw(0x0403, "Could Not initialize Humidity Sensor communications", "Humidity.py", 40)
                # Throw "ADC Could not initialize"
                Error.throw(0x0001, "Failed to initialize ADC", "Humidity.py", 42)
                self.critical_status = True

    # Reads raw ADC value
    def readRaw(self):
        # Reading twice per the Adafruit Documentation,
        # which warns of a bug if you neglect to read
        # twice
        reading = 0
        if self.critical_status:
            return 0
        try:
            reading = ADC.read(self._pin)
            reading = ADC.read(self._pin) * 1.8  # To get voltage
        except:
            # Throw "Could not get reading"
            Error.throw(0x0401)
        if reading < 0:
            # Throw "Reading Invalid"
            Error.throw(0x0402, "Humidity Reading Invalid", "Humidity.py", 61)
        return reading

    # Reads calibrated raw values
    def getValue(self):
        return self._m * self.readRaw() + self._int

    # Sets linear calibration constants for read()
    # slope = slope of linear calibration;
    # i = intercept of linear calibration.
    def setup(self, slope=_m, i=_int):
        self._m = slope
        self._int = i

    def getDataForPacket(self):
        data = int(self.getValue() * 1023)
        return Util.long_to_byte_length(data, 2)
