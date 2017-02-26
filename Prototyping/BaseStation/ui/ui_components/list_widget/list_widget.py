from PyQt4 import QtGui, QtCore


class ListWidget(QtGui.QListWidget):

    count = 0
    markers = []
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
        #marks = self.map.markers

        # Clear the list
        self.clear()

        # Add all markers that aren't rover == True to the list
        l = QtCore.QStringList()
        for i in range(0, len(self.markers)):
            s = QtCore.QString(str(self.markers[i][0]) + ", " + str(self.markers[i][1]))
            l.append(s)

        #print self.markers

        self.addItems(l) #adds elements from the list widget in order

    def add_to_ui(self, lat, long):
        self.markers.append((lat, long))
        #self.count += 1
        self.update_ui()

    #manually remove the
    def remove_from_ui(self, lat, long):
        # marks = self.map.markers
        length = len(self.markers)
        index = -1
        for i in range(0, length):
            #print(lat, long)
            #print i
            if self.markers[i][0] == lat and self.markers[i][1] == long:
                index = i
                #self.markers.pop(i)
                #length = length - 1
        if index is not -1:
            self.markers.pop(index)
        self.update_ui()
