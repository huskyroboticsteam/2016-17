from PyQt4 import QtGui, QtCore


class SensorData(QtGui.QWidget):

    picture_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # Populated with keys from self.map to the QtLabel objects indicating activity
        self.ui_map = {}  # dictionary object
        self.picture = QtGui.QPushButton()
        self.picture.setText("Take a Picture!")
        self.picture.clicked.connect(self.take_picture)
        self.position_slider = QtGui.QSlider()
        self.position_slider.setMaximum(100)
        self.position_slider.setMinimum(0)
        self.position_slider.setOrientation(0x1)
        self.speed_slider = QtGui.QSlider()
        self.speed_slider.setMaximum(100)
        self.speed_slider.setMinimum(0)
        self.speed_slider.setOrientation(0x1)
        self.cam_focus_slider = QtGui.QSlider()
        self.cam_focus_slider.setMaximum(100)
        self.cam_focus_slider.setMinimum(0)
        self.cam_focus_slider.setOrientation(0x1)
        self.rotate_armature_box = QtGui.QCheckBox()

        self.setLayout(self.build_list())

    def take_picture(self):
        self.picture_signal.emit()

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

        # the sliders for position, speed, and camera focus

        self.position_slider.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed))
        self.position_label = QtGui.QLabel()
        self.position_slider.valueChanged.connect(self.update_labels)
        self.position_label.setText("Distance from Ground: " + str(self.position_slider.value()))
        vbox.addWidget(self.position_label)
        vbox.addWidget(self.position_slider)

        self.speed_slider.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed))
        self.speed_label = QtGui.QLabel()
        self.speed_slider.valueChanged.connect(self.update_labels)
        self.speed_label.setText("Rotational speed: " + str(self.speed_slider.value()))
        vbox.addWidget(self.speed_label)
        vbox.addWidget(self.speed_slider)

        self.cam_focus_slider.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed))
        self.cam_focus_label = QtGui.QLabel()
        self.cam_focus_slider.valueChanged.connect(self.update_labels)
        self.cam_focus_label.setText("Camera focus: " + str(self.cam_focus_slider.value()))
        vbox.addWidget(self.cam_focus_label)
        vbox.addWidget(self.cam_focus_slider)

        self.rotate_armature_label = QtGui.QLabel()
        self.rotate_armature_box.stateChanged.connect(self.update_labels)
        self.rotate_armature_label.setText("Rotate armature: " + str(self.rotate_armature_box.isChecked()))
        vbox.addWidget(self.rotate_armature_label)
        vbox.addWidget(self.rotate_armature_box)

        vbox.setAlignment(QtCore.Qt.AlignTop)
        return vbox

    # update the values on labels
    def update_labels(self):
        self.position_label.setText("Distance from Ground: " + str(self.position_slider.value()))
        self.speed_label.setText("Rotational speed: " + str(self.speed_slider.value()))
        self.cam_focus_label.setText("Camera focus: " + str(self.cam_focus_slider.value()))
        self.rotate_armature_label.setText("Rotate armature: " + str(self.rotate_armature_box.isChecked()))

