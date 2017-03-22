"""
Class made to store utility methods
for the EE Science Team

Husky Robotics 2017

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu

Tested/Untested states of methods are given in
method comments below.

"""


class Util:

    ADC_SETUP = False

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

    """
    Returns an integer string of the given number
    formatted in binary with the number of bits
    (default is 8) EG bindigits(7,8) returns
    '00000111'.
    n = signed integer value to convert into binary
    bits = number of bits to represent n (default = 8)
    * If 'n' cannot be represented in 'bits' number of
    bits, it will return a string with the smallest
    number of bits needed to represent 'n'
    TESTED? Yes
    """
    @classmethod
    def inttobin(cls, n, bits=8):
        return ('{0:0' + str(bits) + 'b}').format(n)

    """
    Returns the status of the ADC configuration on board the
    Beaglebone. *DOES NOT COMMUNICATE WITH THE ADC SYSTEM; MUST BE USED
    IN COHERENCE WITH 'setADC_Status()' IN ORDER TO ACHIEVE EXPECTED
    RESULTS.

    Returns:
    True if 'setADC_Status()' was last set to True
    False if 'setADC_Status()' was last set to False
    TESTED? No
    """
    @classmethod
    def ADC_Status(cls):
        return cls.ADC_SETUP

    """
    Sets the status of the on board ADC to the given boolean value.
    * Stored setup value is False be default
    TESTED? No
    """
    @classmethod
    def setADC_Status(cls, status):
        cls.ADC_SETUP = status

    """
    Returns true if 'value' is an integer greater than 0
    TESTED? No
    """
    @classmethod
    def isValidUnsigned(cls, value):
        return isinstance(value, int) and value > 0


