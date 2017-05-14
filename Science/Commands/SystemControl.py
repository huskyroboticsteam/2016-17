import os
import time
import Parse
import Error
import Adafruit_BBIO.GPIO as GPIO  # Ignore compiler errors
from Command import Command
from Packet import SysCtrlID, CameraID


class SystemControl(Command):

    microscopeTriggerTime = 0.01  # Time for microscope to trigger in seconds

    def __init__(self, microscopeRelayPin):
        self.microscopeRelayPin = microscopeRelayPin
        try:
            GPIO.setup(self.microscopeRelayPin, GPIO.OUT)
        except:
            # Throw "Could not setup DIO Pin"
            Error.throw(0x0002)
        Command.__init__(self)

    def initialize(self):
        GPIO.output(self.microscopeRelayPin, GPIO.LOW)

    def run(self, reading):
        PING = Parse.sys_ctrl[SysCtrlID.Ping + 1] == 1
        REBOOT = Parse.sys_ctrl[SysCtrlID.Reboot + 1] == 1
        MICROSCOPE_CAPTURE = Parse.cam_ctrl[CameraID.Microscope]
        MICROSCOPE_AF_CAPTURE = Parse.cam_ctrl[CameraID.Microscope_AF]
        Parse.sys_ctrl[SysCtrlID.Ping + 1] = 0
        Parse.sys_ctrl[SysCtrlID.Reboot + 1] = 0
        Parse.cam_ctrl[CameraID.Microscope + 1] = 0
        if PING:
            if not Error.areErrors():
                Error.throw(0x0000)
            else:
                Error.throw(0x00FE)
        if REBOOT:
            os.system("sudo reboot")
        if MICROSCOPE_CAPTURE:
            GPIO.output(self.microscopeRelayPin, GPIO.HIGH)
            time.sleep(self.microscopeTriggerTime)
            GPIO.output(self.microscopeRelayPin, GPIO.LOW)
        if MICROSCOPE_AF_CAPTURE:
            GPIO.output(self.microscopeRelayPin, GPIO.HIGH)
            time.sleep(2 * self.microscopeTriggerTime)
        time.sleep(0.02)
