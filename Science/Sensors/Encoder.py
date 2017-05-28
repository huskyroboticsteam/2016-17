"""
WARNING: Brian Dai wrote this.
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

TODO: ADD ERROR THROWING TO INITIALIZATION / READ GPIO

"""
import Util
import Adafruit_BBIO.GPIO as GPIO
from math import pi
from threading import Thread
from Sensor import Sensor


class Encoder(Sensor):

    STOP_JOIN_T_CONST = 0.02  # Seconds

    # Takes in channel A and B pin numbers
    # ppr = Pulses per revolution
    def __init__(self, pinA, pinB, ppr):
        self._pinA = pinA      # integer value for A channel
        self._pinB = pinB      # integer value for B channel
        GPIO.setup(self._pinA, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # sets input GPIO pins
        GPIO.setup(self._pinB, GPIO.IN, pull_up_down=GPIO.PUD_OFF)  # sets input GPIO pins
        self._ppr = float(ppr) # pulses per revolution of the encoder
        self._steps = 0        # signed number of steps/pulses encoder has recorded
        self._distK = 1        # K Constant for distance multiplication
        self._angleK = 1       # K Constant for angle multiplication
        self._lastA = False    # last pin position for channel A
        self._lastB = False    # last pin position for channel B
        self._isSetup = False  # whether the Encoder has been set up yet
        self._threadA = None
        self._threadB = None
        self._setup()

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

    def _threadAChannel(self):
        while True:
            self._waitForEdge(self._pinA)

    def _threadBChannel(self):
        while True:
            self._waitForEdge(self._pinB)
    
    def _waitForEdge(self, pin):
        current = GPIO.input(pin)
        if current:
            GPIO.wait_for_edge(pin, GPIO.FALLING)
        else:
            GPIO.wait_for_edge(pin, GPIO.RISING)
        self._update()

    # Updates encoder values
    # Assumes the Encoder does not go past a whole phase change
    def _update(self):
        # Calculates the change in pulses from
        # last cycle to this cycle.
        if not self._isSetup:
            self._setup()

        # Get current readings from GPIO
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

    # Takes in RADIUS of encoder shaft (or gear) to calculate the distance travelled
    # by the encoder wheel. Useful for measuring distance relative to the starting position
    # / the last time reset() was called
    def setDistanceK(self, radius):
        self._distK = 2*pi*radius / self._ppr

    def setAngleK(self, angleK):
        self._angleK = angleK

    # Returns current angle of encoder in radians
    # (-inf, inf) (I.E. not mod 2pi)
    def getAngle(self):
        return self._steps * (2 * pi/self._ppr)  * self._angleK

    def getAngleBounded(self, maxAngle, units='radians'):
        angle = self.getAngle()
        if units=='degrees':
            angle *= 180.0 / pi
        return angle % maxAngle

    def getAngleDegrees(self):
        return self.getAngle() * (180.0 / pi)
   
    def getAngleInNegativeRange(self):
        angle = 180.0 - self.getAngleBounded(360.0, 'degrees')
        if angle == -180:
            angle *= -1
        return angle
    
    # Returns true if the direction the encoder is moving clockwise
    def _isClockwise(self, lastA, lastB, curA, curB):
        return not ((curA != lastA and curA != curB) \
                or (curB != lastB and curA == curB))

    # Returns distance moved as though it were a disk with radius r
    # set in self.setDistanceK(...)
    def getDistance(self):
        return self._steps * self._distK

    # Resets all accumulations
    def reset(self):
        self._steps = 0

    def getValue(self):
        return self.getAngleBounded(360.0, 'degrees'), self.getDistance()

    def getDataForPacket(self):
        angle = int(round(self.getAngle(), 2)) * 100
        return Util.long_to_byte_length(angle, 2)
    
    def stop(self):
        global STOP_JOIN_T_CONST
        self._threadA.join(STOP_JOIN_T_CONST)
        self._threadB.join(STOP_JOIN_T_CONST)

