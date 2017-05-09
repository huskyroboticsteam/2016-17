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
import sys
import math
from binascii import unhexlify

ADC_STATUS = False

"""
Maps a number from one range into another
number = input,
fromLow = lower bound of originating range,
fromHigh = upper bound of originating range,
toLow = lower bound of new range,
toHigh = upper bound of new range
TESTED? [YES]
"""
def map(input, fromLow, fromHigh, toLow, toHigh):
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
def inttobin(n, bits=8):
    return ('{0:0' + str(bits) + 'b}').format(n)

"""
Returns an int with binary length = 'bits'
n = signed integer value to convert into binary
bits = number of bits to represent n (default = 8)
* If 'n' cannot be represented in 'bits' number of
bits, it will return a binary int with the smallest
number of bits needed to represent 'n'
TESTED? Yes
"""
def byteMap(data, bits=8):
    digits = binaryLength(data)
    if digits < bits:
        return data << int(bits - digits)
    else:
        return data

"""
Returns necessary binary length of base-10 integer n.
TESTED? YES
"""
def binaryLength(n):
    if n > 0:
        digits = int(math.log(n, 2)) + 1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log(-n, 2)) + 2
    return int(digits)

"""
Returns an integer from a hex encoded bytearray
called data. From position start to stop
"""
def intFromHexRange(data, start, stop):
    return int(str(data[start:stop]).encode('hex'), 16)

"""
Copied from StackOverflow
Takes in long of val and converts
it into a char string to represent
the data.
TESTED? YES
"""
def long_to_bytes(val, endianness='big'):
    """
    Use :ref:`string formatting` and :func:`~binascii.unhexlify` to
    convert ``val``, a :func:`long`, to a byte :func:`str`.

    :param long val: The value to pack

    :param str endianness: The endianness of the result. ``'big'`` for
      big-endian, ``'little'`` for little-endian.

    If you want byte- and word-ordering to differ, you're on your own.

    Using :ref:`string formatting` lets us use Python's C innards.
    """

    # one (1) hex digit per four (4) bits
    width = val.bit_length()

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    width += 8 - ((width % 8) or 8)

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    s = unhexlify(fmt % val)

    if endianness == 'little':
        # see http://stackoverflow.com/a/931095/309233
        s = s[::-1]

    return s

"""
Returns string of bits
given an string of characters
TESTED? YES
"""
def chartobytes(val):
    ret_val = ""
    for n in val:
        this_val = bin(ord(n))[2:]
        if len(this_val) % 8 != 0:
            this_val = "00000000"[0:(8-(len(this_val) % 8))] + this_val
        ret_val += this_val
    return ret_val


"""
Takes binary string n (length 8 bits)
and converts to ASCII
TESTED? Yes
"""
def bintochr(n):
    return chr(int(n, 2))


"""
Takes binary string of any
length and converts it to
string of chars representing
that binary data
TESTED? Yes
"""
def full_bin_to_chr(n):
    ret_val = ""
    if len(n) % 8 != 0:
        n += "00000000"[0:8-(len(n) % 8)]
    while len(n) != 0:
        ret_val += bintochr(n[0:8])
        n = n[8:]
    return ret_val


"""
Reverses bits given an integer n,
outputs result as an integer
Tested? Yes
"""
def reverseBits(n):
    return int(bin(n)[:1:-1], 2)

"""
Returns the status of the ADC configuration on board the
Beaglebone. *DOES NOT COMMUNICATE WITH THE ADC SYSTEM; MUST BE USED
IN COHERENCE WITH 'setADC_Status()' IN ORDER TO ACHIEVE EXPECTED
RESULTS.

Returns:
True if 'setADC_Status()' was last set to True
False if 'setADC_Status()' was last set to False
TESTED? Yes
"""
def ADC_Status():
    global ADC_STATUS
    return ADC_STATUS


"""
Sets the status of the on board ADC to the given boolean value.
* Stored setup value is False be default
TESTED? No
"""
def setADC_Status(status):
    global ADC_STATUS
    ADC_STATUS = status


"""
Returns true if 'value' is an integer greater than 0
TESTED? No
"""
def isValidUnsigned(value):
    return isinstance(value, int) and value > 0


