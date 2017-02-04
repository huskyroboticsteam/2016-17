import sys
from PyQt4.QtCore import *
import Map
from PyQt4.QtGui import *


class command(QLineEdit):
    def __init__(self, map, parent = None):
        super(command, self).__init__(parent)

        self.map = map
        # app = QApplication(sys.argv)
        commands = ("add", "remove", "set")

        # layout = QFormLayout()
        text, ok = self.getText(self, 'Text Input Dialog', 'Enter your name:')
        if ok:
            list = text.split(" ")
            if list[0] not in commands:
                print list[0] + " isn't a command"
            else:
                self.execute(list)

    def blah(self):
        print

    def execute(self, list):
        print "go"
        if (list[0] == "add"):
            # type add lat long
            self.map.add_marker(list[1], list[2])
            print "adding"
        elif (list[0] == "remove"):
            print "removing"
        elif (list[0] == "set"):
            print "setting"

