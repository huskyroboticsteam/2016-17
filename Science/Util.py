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
import struct
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
def bytesToInt(data, start=None, stop=None, signed=False):
    """Convert a bytearray into an integer, considering the first bit as
    sign. The data MUST be big-endian."""
    data = data[start:stop]
    if signed:
        negative = data[0] & 0x80 > 0

        if negative:
            inverted = bytearray(~d % 256 for d in data)
            return -signedbytes(inverted) - 1

    encoded = str(data).encode('hex')
    return int(encoded, 16)

"""
Returns val represented as a bytearray length byte_length
DEFINITELY WORKS!
"""
def long_to_byte_length(val, byte_length, endianness='big'):
    valBA = bytearray(long_to_bytes(val))
    if len(valBA) > byte_length:
        valBA = valBA[:byte_length]
    elif len(valBA) < byte_length:
        valBA = b'\x00'*(byte_length-len(valBA)) + valBA
    return valBA

"""
Appends Bytearray to end of parent bytearray
"""
def appendBytearray(parent, other):
    for i in other:
        parent.append(i)
    return parent

"""
Copied from StackOverflow
Added Zero-Case check
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

    # Negative case check
    if val < 0:
        return struct.pack('<l', val)

    # Check zero case
    if val == 0:
        return '\x00'

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
TESTED? Yes
"""
def isValidUnsigned(value):
    return isinstance(value, int) and value > 0

"""
Returns true if 'value' is a signed integer 
in the bit-width range b using two's complement
Tested? Yes
"""
def isValidSigned(value, b=32):
    if not isinstance(value, int):
       return False
    max = 2**b - 1
    min = -(max + 1)
    return value >= min and value <= max


"""
Writes string to console. Attempts non-string to string conversion.
Adds a new line at the end
"""
def write(val):
    sys.stdout.write(str(val) + "\n")
