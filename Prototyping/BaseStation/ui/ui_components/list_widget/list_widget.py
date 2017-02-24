from PyQt4 import QtGui, QtCore


class ListWidget(QtGui.QListWidget):

    signalStatus = QtCore.pyqtSignal([str])

    def __init__(self, map):
        super(self.__class__, self).__init__()


        self.map = map
        self.setMaximumHeight(75)

        # Force it to be smaller than the map
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        self.setSizePolicy(policy)

        self.itemDoubleClicked.connect(self.editing_item)

    def editing_item(self, item):
        # self.currentRow() # Gives the index in the list
        cmd = 'update %s %s' %(self.currentItem().text(), self.currentRow() + 1)
        cmd = cmd.replace(',', '')
        self.signalStatus.emit(cmd)
        # print cmd

        # TODO: emit a signal so the command line can set this data

    # Updated by command.py
    def update_ui(self):
        marks = self.map.markers

        # Clear the list
        self.clear()

        # Add all markers that aren't rover == True to the list
        l = QtCore.QStringList()
        for i in range(0, len(marks)):
            if marks[i].rover is False:
                s = QtCore.QString(str(marks[i].coordX) + ", " + str(marks[i].coordY))
                l.append(s)

        self.addItems(l)
