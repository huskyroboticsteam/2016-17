from PyQt4 import QtGui, QtCore


class SensorData(QtGui.QWidget):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # Populated with keys from self.map to the QtLabel objects indicating activity
        self.ui_map = {}  # dictionary object
        self.picture = QtGui.QPushButton()
        self.picture.setText("Take a Picture!")

        self.setLayout(self.build_list())

    def update_ui(self, dictionary):
        """
        Update all sensor values with the ones from the dictionary
        :param dictionary: A map of the friendly names to the sensor value
        :return: None
        """
        for key in dictionary:
            self.ui_map[key].setText(dictionary[key])

    def build_list(self):
        """
        Builds the initial list to the screen
        Maps the friendly name to the label we update with the sensor value
        :return: The QVBoxLayout to add to the widget window
        """
        dictionary = ["Potentiometer", "Magnetometer", "Drive Encoder 1", "Drive Encoder 2", "Drive Encoder 3", "Drive Encoder 4"]
        science_sensors = ["Distance", "UV", "Thermo Internal", "Thermo External", "Humidity", "Science Encoder 1", "Science Encoder 2", "Science Encoder 3", "Limit Switch"]
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

        science_label = QtGui.QLabel()
        science_label.setText("Science Sensors")
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        science_label.setFont(font)
        vbox.addWidget(science_label)

        for key in science_sensors:
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

        vbox.addWidget(self.picture)

        vbox.setAlignment(QtCore.Qt.AlignTop)
        return vbox


