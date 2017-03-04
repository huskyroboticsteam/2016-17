from PyQt4 import QtCore
from PyQt4.QtGui import *


class command(QLineEdit):
    signalStatus = QtCore.pyqtSignal([tuple])
    autoTrigger = QtCore.pyqtSignal(bool)

    def __init__(self, map, sock, list_wid, parent = None):
        super(command, self).__init__(parent)

        self.map = map
        self.sock = sock
        self.list_wid = list_wid
        self.commands = ("ADD", "REMOVE", "UPDATE", "AUTO")

    def focusInEvent(self, e):
        super(self.__class__, self).focusInEvent(e)

        print "In"

    def focusOutEvent(self, e):
        super(self.__class__, self).focusOutEvent(e)

        print "Out"

    def keyPressEvent(self, e):  # e is event
        super(command, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Return:
            list = self.text().split(" ")  # text() gets the current texts inside the editor
            if str(list[0]).upper() not in self.commands:  # check if user enters a valid command
                print list[0] + " isn't a command"
            else:
                self.setText("")  # refreshes the text editor to blank
                self.execute(list)

    def execute(self, list):
        """
        :param list (list of strings): User input

        Depending on list[0], add, remove, update, or auto
        Add: Adds marker to map
        Remove: Remove marker from map
        Update: Update marker location
        Auto: Turn on auto-mode
        """
        cmd = str(list[0]).upper()
        if (cmd == self.commands[0]): # Add
            # type add lat long
            self.map.add_marker(list[1], list[2])
            self.list_wid.update_ui()
        elif (cmd == self.commands[1]): # Remove
            self.map.remove_marker(int(list[1]) - 1) # index
            self.list_wid.update_ui()
        elif (cmd == self.commands[2]): # Update
            self.map.update_marker(list[1], list[2], int(list[3]) - 1) # long, lat, index
            self.list_wid.update_ui()
        elif (cmd == self.commands[3]): # Auto
            comms = self.sock

            # Don't send the data again if we are in auto mode
            if comms.auto is False:
                self.autoTrigger.emit(False)
                comms.open_tcp()
                for i in range(0, len(self.markers)):
                    lat = self.markers[i].coordX.toAscii()
                    long = self.markers[i].coordY.toAscii()
                    lat = float(lat)
                    long = float(long)

                    if i == len(self.markers) - 1:
                        self.signalStatus.emit(False, lat, long)
                    else:
                        self.signalStatus.emit(True, lat, long)
                comms.auto = True
                comms.close_tcp()
            else:
                self.autoTrigger(True)
                comms.auto = False

    def update(self, cmd):
        self.setText(cmd)