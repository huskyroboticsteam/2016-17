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


TODO: ADD ERROR THROWING TO INITIALIZED / READ GPIO

"""
import Util
import Adafruit_BBIO.GPIO as GPIO
from math import pi
from threading import Thread
from Sensor import Sensor


class Encoder(Sensor):

    # Takes in channel A and B pin numbers
    # ppr = Pulses per revolution
    def __init__(self, pinA, pinB, ppr):
        self._pinA = pinA      # integer value for A channel
        self._pinB = pinB      # integer value for B channel
        GPIO.setup(self._pinA, GPIO.IN)  # sets input GPIO pins
        GPIO.setup(self._pinB, GPIO.IN)  # sets input GPIO pins
        self._ppr = ppr        # pulses per revolution of the encoder
        self._steps = 0        # signed number of steps/pulses encoder has recorded
        self._distK = 1        # K Constant for distance multiplication
        self._lastA = False    # last pin position for channel A
        self._lastB = False    # last pin position for channel B
        self._isSetup = False  # whether the Encoder has been set up yet
        self._threadA = None
        self._threadB = None

    # Initializes Encoder
    # Meant for internal use only
    def _setup(self):
        self._lastA = GPIO.input(self._pinA)
        self._lastB = GPIO.input(self._pinB)
        self._isSetup = True
        self._threadA = Thread(target=self._threadAChannel)
        self._threadB = Thread(target=self._threadBChannel)
        self._threadA.start()
        self._threadB.start()

    # Updates encoder values
    # Assumes the Encoder does not go past a whole phase change
    def _update(self):
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

    def _waitForEdge(self, pin):
        current = GPIO.input(pin)
        if current:
            GPIO.waitForEdge(pin, GPIO.FALLING)
        else:
            GPIO.waitForEdge(pin, GPIO.RISING)
        self._update()

    def _waitForA(self):
        self._waitForEdge(self._pinA)

    def _waitForB(self):
        self._waitForEdge(self._pinB)

    # This method sets a constant whose product with the accumulated angle is
    # the distance traveled
    def setDistanceK(self, distK):
        self._distK = distK

    # Returns current angle of encoder in radians
    # (-inf, inf) (I.E. not mod 2pi)
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

    def _threadAChannel(self):
        while True:
            self._waitForA()

    def _threadBChannel(self):
        while True:
            self._waitForB()

    def getValue(self):
        return self.getAngle(), self.getDistance()

    def getDataForPacket(self):
        return Util.inttobin(round(self.getAngle() % (2*pi)), 16)

    def stop(self):
        self._threadA.join(0.02)
        self._threadB.join(0.02)

