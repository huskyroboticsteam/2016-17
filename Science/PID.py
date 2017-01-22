import time

class PID(object):

    _lastError = 0
    _lastTime = 0
    _output = 0
    _pVal = 0
    _iVal = 0
    _dVal = 0

    def __init__(self, kP, kI, kD):
        self._p = kP
        self._i = kI
        self._d = kD

    def setTarget(self, target):
        self._target = target

    def run(self, input):
        curTime = time.time()
        dT = curTime - self._lastTime
        error = self._target - input
        self._pVal = self._p * error
        self._iVal += self._i * (dT * (self._lastError - error))
        self._dVal = self._d * ( (self._lastError - error) / dT )
        self._lastError = error
        self._lastTime = curTime
        self._output = self._pVal + self._iVal + self._dVal

    def getOutput(self):
        return self._output
