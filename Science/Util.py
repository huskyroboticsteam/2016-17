"""
Class made to store utility methods
for the EE Science Team

Husky Robotics 2017
"""


class Util(object):

    """
    Maps a number from one range into another
    number = input,
    fromLow = lower bound of originating range,
    fromHigh = upper bound of originating range,
    toLow = lower bound of new range,
    toHigh = upper bound of new range
    TESTED? [YES]
    """
    @staticmethod
    def map(input, fromLow, fromHigh, toLow, toHigh):
        return toLow + ((float(input - fromLow)/(fromHigh - fromLow)) * (toHigh - toLow))

    @staticmethod
    def updateEncoders(encoders):
        for encoder in encoders:
            encoder.update()
