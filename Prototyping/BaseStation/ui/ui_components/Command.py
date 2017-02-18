import sys
from PyQt4 import QtCore
from PyQt4.QtGui import *
import command_api


class command(QLineEdit):
    def __init__(self, map, parent = None):
        super(command, self).__init__(parent)

        self.map = map
        self.commands = ("add", "remove", "set", "AUTO")
        print self.isReadOnly()
        #using self makes this a class variable

    def keyPressEvent(self, e): #e is event
        self.setText(self.text() + str(e.key()))
        if e.key() == QtCore.Qt.Key_Enter:
            list = self.text().split(" ") #text() gets the current texts inside the editor
            if list[0] not in self.commands: #check if user enters a valid command
                print list[0] + " isn't a command"
            else:
                self.setText("") #refreshes the text editor to blank
                self.execute(list)

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
        elif (list[0] == "AUTO"):
            command_api.send_auto_data(self.map.markers)


