__author__ = 'Trevor'

# Class that stores "half" of a single map coordinate - either latitude or longitude in decimal format, degree-minute format, or degree-minute-second format.
# For example, Seattle is at latitude 47 deg, 39 min, and 13.7268 sec, and longitude -122 deg, 18 min, 28.206 sec. This can also be represented as 47.653813, -122.307835.
# There is also degree-minute format, where degrees are given as an integer and then minutes as a decimal value (instead of minutes as an integer and then seconds as a decimal value).
# This class will store the latitude or longitude in whatever format is given as input.
# This is useful because we are given degree-minute format coordinates of gates and points of interest at URC, but decimal values are easiest to work with in math.

# Software Team's job: replace this with something better that stores both latitude and longitude, and converts values to decimal automatically upon initialization.
class degreeMinSec:
    def __init__(self, degree, minute = 0.0, seconds = 0.0): # If minutes or seconds unprovided, go without. The minute and second arguments are optional: if not provided, use the value after the equals sign.
        if(degree == ""):
            self.degrees = "0"
        else:
           self.degrees = degree
        if(minute == ""):
            self.min = "0"
        else:
            self.min = minute
        if(seconds == ""):
            self.sec = "0"
        else:
            self.sec = seconds

    # If this function called, convert the stored coordinates to decimal. Used in last year's GUI program so mathy stuff can be performed on coordinates.
    # This year we'll want to auto-convert coords to decimal values upon entry.
    def toDecimal(self):
        if self.degrees > 0.0: # If degrees value is positive, add minutes and seconds.
            result = float(self.degrees) + (float(self.min) / 60.0) + (float(self.sec) / 3600.0)
        if self.degrees <= 0.0: # If degrees value is negative, need to subtract minutes and seconds.
            result = float(self.degrees) - (float(self.min) / 60.0) - (float(self.sec) / 3600.0)
        return result

