from PyQt4 import QtGui, QtCore


class ListWidget(QtGui.QListWidget):

    """
    Mirrors the marker list maintained by the Map object while ignoring the rover marker
    Emits signals that are picked up by other parts of the UI such as the COMMAND module
    """

    count = 0
    markers = []
    callToDelete = QtCore.pyqtSignal(int)
    highlightMarker = QtCore.pyqtSignal(int)
    replaceMarker = QtCore.pyqtSignal(int)

    giveMarkers = QtCore.pyqtSignal(list)

    def __init__(self):
        super(self.__class__, self).__init__()

        self.setMaximumHeight(75)

        # Force it to be smaller than the map
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        self.setSizePolicy(policy)
        self.index = None
        self.itemClicked.connect(self.highlight_marker)

    def keyPressEvent(self, key):
        if key.key() == QtCore.Qt.Key_Delete:
            self.callToDelete.emit(self.currentRow())
            self.remove_from_ui(self.currentRow())

    def highlight_marker(self, item):
        self.highlightMarker.emit(self.currentRow())

    # Updates the list by changing an array of markers into a list of strings
    def update_ui(self):

        # Clear the list
        self.clear()

        # Add all markers that aren't rover == True to the list
        l = QtCore.QStringList()
        for i in range(0, len(self.markers)):
            s = QtCore.QString(str((i + 1)) + " " + str(self.markers[i][0]) + ", " + str(self.markers[i][1]))
            l.append(s)

        self.addItems(l)  # adds elements from the list widget in order

    # Called when things are added to the marker list
    # Marked for removal in Map/List rework
    def add_to_ui(self, lat, long):
        self.markers.append((lat, long))
        self.update_ui()

    # Called when things are removed from the marker list
    # Marked for removal in Map/List rework
    def remove_from_ui(self, index):
        self.markers.pop(index)
        self.update_ui()

    def update_from_ui(self, lat, long, index):
        self.remove_from_ui(index)
        self.markers.insert(index, (lat, long))
        self.update_ui()

    def get_markers(self):
        self.giveMarkers.emit(self.markers)
