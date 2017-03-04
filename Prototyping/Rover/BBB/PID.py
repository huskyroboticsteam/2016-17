import time


class PID(object):
    """
    PID for rover controls, adaption of Science/PID.py
    Used this for reference: https://gist.github.com/chaosmail/8372717

    Attributes:
        _p, _i, _d (float): The constants for the PID controller algorithm.
            Can be fine-tuned.
        _target (float): The desired value for the value controlled. (The setpoint.)
        _lastError (float): The previous error (The value of `_target - actual value).
        _lastTime (float): The time as returned by `time.time()` when `run()`
            was last called.
        _output (float): How the controlled value should be adjusted. Positive
            means that it should be increased.
        _pVal, _iVal, _dVal (float): The three terms in the PID equation.
    """

    def __init__(self, kP, kI, kD):
        """
        Initializes the PID algorithm.

        Args:
            kP, kI, kD (float): The constants for the PID algorithm.
                Can be fine-tuned.
        """
        self._p = float(kP)
        self._i = float(kI)
        self._d = float(kD)
        self._target = 0.0
        self._lastError = 0.0
        self._lastTime = 0.0
        self._output = 0.0
        self._pVal = 0.0
        self._iVal = 0.0
        self._dVal = 0.0

    def setTarget(self, target):
        """
        Set the target value (setpoint)

        Args:
            target (float): The target value.
        """
        self._target = float(target)
        self.reset()

    def run(self, input):
        """
        Advance the PID algorithm by one time step and updates the output.
        Should be periodically called.

        Args:
            input (float): The observed value. (The process variable.)
        """
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
        """
        Clear previous data.
        """
        self._pVal = 0.0
        self._iVal = 0.0
        self._dVal = 0.0
        self._lastError = 0.0

    def getOutput(self):
        """
        Returns:
            float: The output of the PID algorithm. Positive means that the
                value should be increased.
        """
        return self._output

    def setCoefficients(self, kP, kI, kD):
        """
        Changes the constants for the PID algorithm.
        """
        self._p = float(kP)
        self._i = float(kI)
        self._d = float(kD)

    def getTarget(self):
        """
        Returns:
            float: The current target value (setpoint).
        """
        return self._target