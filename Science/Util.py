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
    return ('{0:0' + str(bits) + 'b}').format(int(n))


"""
Returns string of bits
given an integer value
TESTED? Yes
"""
def chartobytes(n):
    ret_val = bin(n)
    ret_val = ret_val[2:]
    if len(ret_val) % 8 != 0:
        ret_val = "00000000"[0:8 - (len(ret_val) % 8)] + ret_val
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
Returns the status of the ADC configuration on board the
Beaglebone. *DOES NOT COMMUNICATE WITH THE ADC SYSTEM; MUST BE USED
IN COHERENCE WITH 'setADC_Status()' IN ORDER TO ACHIEVE EXPECTED
RESULTS.

Returns:
True if 'setADC_Status()' was last set to True
False if 'setADC_Status()' was last set to False
TESTED? No
"""
def ADC_Status():
    return ADC_SETUP


"""
Sets the status of the on board ADC to the given boolean value.
* Stored setup value is False be default
TESTED? No
"""
def setADC_Status(status):
    ADC_SETUP = status


"""
Returns true if 'value' is an integer greater than 0
TESTED? No
"""
def isValidUnsigned(value):
    return isinstance(value, int) and value > 0


