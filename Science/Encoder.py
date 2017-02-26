"""
WARNING: Brian wrote this.
This code is untested and
has known bugs. Do Not Attempt
to Interface with this class yet.

Class built to interface with Encoder
Based off of the Encoder specs:
http://playground.arduino.cc/Main/RotaryEncoders

Written by Brian Dai in February 2017
Science Team of Husky Robotics
(Untested as of 2/9/2017)

**Built for Real-Time Operation

Basic Implementation as follows:

1) Initialize the Encoder with integer numbers for the A and B channels of the
    Encoder and an integer number for the pulses per revolution of the Encoder
...

NOTE: Only two channel encoders
NOTE: Vibrations that can cause misalignment of the encoder wheel (especially
    in the case of optical encoders) is ignored
NOTE: Run the update() method as often as possible
NOTE: Assumes Encoder does not step more than one phase per update
"""

from math import pi
import Adafruit_BBIO.GPIO as GPIO


class Encoder:

    # Takes in channel A and B pin numbers
    # ppr = Pulses per revolution
    def __init__(self, pinA, pinB, ppr):

        self._pinA = pinA      # integer value for A channel
        self._pinB = pinB      # integer value for B channel
        GPIO.setup(self._pinA, GPIO.IN)  # sets input GPIO pins
        GPIO.setup(self._pinB, GPIO.IN)  # sets input GPIO pins
        self._ppr = ppr        # pulses per revolution of the encoder, default to 1
                               # instead of 0 so nothing breaks upon division
        self._steps = 0        # signed number of steps/pulses encoder has recorded
        self._distK = 1        # K Constant for distance multiplication
        self._lastA = False    # last pin position for channel A
        self._lastB = False    # last pin position for channel B
        self._isSetup = False  # whether the Encoder has been set up yet

    # Initializes Encoder
    # Meant for internal use only
    def _setup(self):
        self._lastA = GPIO.input(self._pinA)
        self._lastB = GPIO.input(self._pinB)
        self._isSetup = True

    # Updates encoder values
    # Assumes the Encoder does not go past a whole phase change
    def update(self):
        # Calculates the change in pulses from
        # last cycle to this cycle.
        if not self._isSetup:
            self._setup()
        curA = GPIO.input(self._pinA)
        curB = GPIO.input(self._pinB)

        increment = 0
        if self._lastA != curA:
            increment += 1
        if self._lastB != curB:
            increment += 1
        if self._isClockwise(self._lastA, self._lastB, curA, curB):
            self._steps += increment
        else:
            self._steps -= increment

        self._lastA = curA
        self._lastB = curB

    def waitForEdge(self):
        pass

    # This method sets a constant whose product with the accumulated angle is
    # the distance traveled
    def setDistanceK(self, distK):
        self._distK = distK

    # Returns current angle of encoder
    # (Does not have to be in range 0 to 360;
    # in fact, probably should be (-inf, inf)
    def getAngle(self):
        return self._steps * (2 * pi/self._ppr)

    # Returns true if the direction the encoder is moving clockwise
    def _isClockwise(self, lastA, lastB, curA, curB):
        return (curA != lastA and curA != curB) \
                or (curB != lastB and curA == curB)

    # Returns distance moved as though it were a disk with radius "_distK"
    # Set "_distK" in self.setDistanceK(...)
    def getDistance(self):
        return self.getAngle() * self._distK

    # Resets all accumulations
    def reset(self):
        self._steps = 0
