"""
Class made to store utility methods
for the EE Science Team

Husky Robotics 2017
"""


class Util:

    """
    Maps a number from one range into another
    number = input,
    fromLow = lower bound of originating range,
    fromHigh = upper bound of originating range,
    toLow = lower bound of new range,
    toHigh = upper bound of new range
    TESTED? [YES]
    """
    @classmethod
    def map(cls, input, fromLow, fromHigh, toLow, toHigh):
        return toLow + ((float(input - fromLow)/(fromHigh - fromLow)) * (toHigh - toLow))

    @classmethod
    def updateEncoders(cls, encoders):
        for encoder in encoders:
            encoder._update()

    @classmethod
    def bindigits(cls, n, bits=8):
        s = bin(n & int("1" * bits, 2))[2:]
        return ("{0:0>%s}" % (bits)).format(s)

    @classmethod
    def inttobin(cls, n, bits=8):
        return ('{0:0' + str(bits) + 'b}').format(n)


