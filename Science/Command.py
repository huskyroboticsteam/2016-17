from threading import Thread


class Command:

    def __init__(self, pid=None):
        self._thread = Thread(target=self._threadRun)
        self._pid = pid
        self._pidCtrl = True
        self._setpoint = 0
        if self._pid is None:
            self._pidCtrl = False

    def start(self):
        self._thread.start()

    def setpoint(self, setpoint=None):
        if not (setpoint is None):
            self._setpoint = setpoint
        return self._setpoint

    def _threadRun(self):
        while not self.isFinished():
            self.run(self._setpoint)

    def stop(self):
        self.stopSafe()
        self._thread.join(0.02)

    def initialize(self):
        pass

    def run(self, reading):
        pass

    def stopSafe(self):
        pass

    def isFinished(self):
        pass