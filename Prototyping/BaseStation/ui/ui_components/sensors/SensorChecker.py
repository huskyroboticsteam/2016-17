from PyQt4 import QtGui, QtCore

class SensorData(QtGui.QWidget):
    def __init__(self, ip_map, update_time, parent=None):
        super(self.__class__, self).__init__(parent)
        self.hasBuilt = False
    # checks whether computer is on same network as rover

    # define an update method that creates static labels and
    # associates each one with a value received from the communications packets

        self.map = ip_map #list of IPS that need to be checked

        # Populated with keys from self.map to the QtLabel objects indicating activity
        self.ui_map = {} #dictionary object

        # self.setLayout(self.build_list())

    def update_ui(self, dictionary):
        #results = self.threaded_ping() # an IP mapped to a boolean
        # print results
        if self.hasBuilt:
            for key in dictionary:
                self.ui_map[key].setText(dictionary[key])

    def build_list(self, dictionary):
        vbox = QtGui.QVBoxLayout()

        for key in dictionary:
            hbox = QtGui.QHBoxLayout()

            label = QtGui.QLabel()
            label.setAlignment(QtCore.Qt.AlignHCenter)
            label.setText(key)

            label2 = QtGui.QLabel()
            label2.setAlignment(QtCore.Qt.AlignHCenter)
            label2.setText("No data")

            hbox.addWidget(label)
            hbox.addWidget(label2)

            vbox.addLayout(hbox)

            self.ui_map[key] = label2  # the keys of the map are IPs

        vbox.setAlignment(QtCore.Qt.AlignTop)
        self.hasBuilt = True;

        return vbox


