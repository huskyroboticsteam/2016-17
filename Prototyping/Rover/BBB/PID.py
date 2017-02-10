import time
'''
PID for rover controls, adaption of Science/PID.py

Use this for reference: https://gist.github.com/chaosmail/8372717
'''

class PID(object):

    def __init__(self, kP, kI, kD):
        self._p = kP
        self._i = kI
        self._d = kD
        self._target = 0
        self._lastError = 0
        self._lastTime = 0
        self._output = 0
        self._pVal = 0
        self._iVal = 0
        self._dVal = 0

    def setTarget(self, target):
        self._target = target
        self.reset()

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

    def reset(self):
        self._pVal = 0
        self._iVal = 0
        self._dVal = 0
        self._lastError = 0

    def getOutput(self):
        return self._output

    def setCoefficients(self, kP, kI, kD):
        self._p = kP
        self._i = kI
        self._d = kD

    def getTarget(self):
        return self._target