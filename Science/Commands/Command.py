from threading import Thread


class Command:

    commands = []

    def __init__(self, pid=None):
        self._thread = Thread(target=self._threadRun)
        self._pid = pid
        self.kp = 0
        self.ki = 0
        self.kd = 0
        if self._pid != None:
            self.kp = self._pid._p
            self.ki = self._pid._i
            self.kd = self._pid._d
        self._pidCtrl = True
        self._setpoint = 0
        Command.commands += [self]
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
            self.run(self.setpoint())

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

    @classmethod
    def initializeAll(cls):
        for command in Command.commands:
            command.initialize()

    @classmethod
    def stopAllSafe(cls):
        for command in Command.commands:
            command.stopSafe()

    @classmethod
    def startAll(cls):
        for command in Command.commands:
            command.start()
