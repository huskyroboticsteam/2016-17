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

    @staticmethod
    def bindigits(n, bits=8):
        s = bin(n & int("1" * bits, 2))[2:]
        return ("{0:0>%s}" % (bits)).format(s)

    @staticmethod
    def inttobin(n, bits=8):
        return '{0:0' + str(bits) + 'b}'.format(n)


