import os
import time
import Parse
import Error
from Command import Command
from Packet import SysCtrlID


class SystemControl(Command):

    def __init__(self):
        Command.__init__(self)

    def run(self, reading):
        PING = Parse.sys_ctrl[SysCtrlID.Ping + 1] == 1
        REBOOT = Parse.sys_ctrl[SysCtrlID.Reboot + 1] == 1
        Parse.sys_ctrl[SysCtrlID.Ping + 1] = 0
        Parse.sys_ctrl[SysCtrlID.Reboot + 1] = 0
        if PING:
            if not Error.areErrors():
                Error.throw(0x0000)
            else:
                Error.throw(0x00FE)
        if REBOOT:
            os.system("sudo reboot")
        time.sleep(1)
