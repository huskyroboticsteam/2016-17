"""
Class built to create a PID control loop in python
Based off of the PID control algorithm:
https://en.wikipedia.org/wiki/PID_controller

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

**Built for Real-Time Operation

Basic Implementation as follows:

1) Choose P, I, and D constants in constructor
2) Set a target value
    (Units do not matter as long as they are used uniformly in the loop)
3) Use run() to run the PID loop given a sensor reading
    (Should be called iteratively, since it depends on system time)
4) Use getOutput() to return the desired output.

NOTE: This output will be relative to the units given in the run() method.
Map this output to a given range if necessary, for example, in using motors.
NOTE: Nothing has to be done to change the target value during operation, it is all handled
in this class.

**IMPORTANT:
A PID Control loop needs to be tuned.
That is, to be used correctly, the P, I, and D
coefficients need to be precisely chosen.

An algorithm for determining coefficients:
https://en.wikipedia.org/wiki/PID_controller#Ziegler.E2.80.93Nichols_method

Let me know if you find a bug or have any recommendations;
I'd rather find out now than later! jadenjb@uw.edu
Thanks!
"""

import time


class PID:

    # Initializes coefficients and sets target to 0
    def __init__(self, kP, kI, kD):
        self.setCoefficients(kP, kI, kD)
        self._target = 0
        self._lastError = 0
        self._lastTime = 0
        self._output = 0
        self._pVal = 0
        self._iVal = 0
        self._dVal = 0

    # Set target of control loop.
    # **Can be changed during operation without consequence
    def setTarget(self, target):
        self._target = target
        self._reset()

    # Runs PID Algorithm
    # Designed to be ran iteratively
    def run(self, input):
        curTime = time.time()
        dT = curTime - self._lastTime
        error = self._target - input
        self._pVal = self._p * error
        self._iVal += self._i * (dT * error)
        self._dVal = self._d * ((error - self._lastError) / dT)
        self._lastError = error
        self._lastTime = curTime
        self._output = self._pVal + self._iVal + self._dVal
        self._output = self.restrainOutput(self._output)

    # Resets current accumulations of the PID
    # Meant for internal (private) use only
    def _reset(self):
        self._pVal = 0
        self._iVal = 0
        self._dVal = 0
        self._lastError = 0

    # Returns last accumulated output for the PID loop
    def getOutput(self):
        return self._output

    # Sets coefficients of the PID
    # Can be used externally if needed,
    # but is not recommended.
    def setCoefficients(self, kP, kI, kD):
        self._p = kP
        self._i = kI
        self._d = kD

    # Restrains output to (+/-)1
    def restrainOutput(self, output):
        if output > 1:
            return 1
        if output < -1:
            return -1
        return output
