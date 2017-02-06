from PyQt4.QtGui import *
from PyQt4 import QtCore


class command(QLineEdit):
    def __init__(self, map, parent=None):
        super(command, self).__init__(parent)
        self.map = map
        self.commands = ("add", "remove", "set")

    def keyPressEvent(self, e):
        # Call the super method so we can type in the box
        super(command, self).keyPressEvent(e)

        # Added functionality
        if e.key() == QtCore.Qt.Key_Return:
            print "Run"
            list = self.text().split(" ")
            if list[0] not in self.commands:
                print list[0] + " isn't a command"
            else:
                self.setText("")
                self.execute(list)

    def execute(self, list):
        print "go"
        if list[0] == "add":
            # type add lat long
            self.map.add_marker(list[1], list[2])
            print "adding"
        elif list[0] == "remove":
            print "removing"
        elif list[0] == "set":
            print "setting"

