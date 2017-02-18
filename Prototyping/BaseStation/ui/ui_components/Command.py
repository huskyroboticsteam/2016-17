from PyQt4 import QtCore
from PyQt4.QtGui import *
import command_api


class command(QLineEdit):
    def __init__(self, map, parent = None):
        super(command, self).__init__(parent)

        self.map = map
        self.commands = ("ADD", "REMOVE", "SET", "AUTO")

    def keyPressEvent(self, e): #e is event
        super(command, self).keyPressEvent(e)

        if e.key() == QtCore.Qt.Key_Return:
            list = self.text().split(" ") #text() gets the current texts inside the editor
            if list[0] not in self.commands: #check if user enters a valid command
                print list[0] + " isn't a command"
            else:
                self.setText("") #refreshes the text editor to blank
                self.execute(list)

    def execute(self, list):
        if (list[0] == "ADD"):
            # type add lat long
            self.map.add_marker(list[1], list[2])
        elif (list[0] == "REMOVE"):
            self.map.remove_marker(int(list[1]) - 1)
        elif (list[0] == "AUTO"):
            command_api.send_auto_data(self.map.markers)


