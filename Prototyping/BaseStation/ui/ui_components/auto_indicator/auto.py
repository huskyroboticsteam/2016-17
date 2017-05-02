from PyQt4 import QtGui, QtCore


class Auto(QtGui.QWidget):
    """
        A simple widget that displays the text "AUTO" or displays nothing
    """

    # Expects auto comms status, connection open?
    enableAutoTrigger = QtCore.pyqtSignal(bool, bool)
    requestMarkers = QtCore.pyqtSignal()
    sendData = QtCore.pyqtSignal(bool, float, float)

    def __init__(self):
        super(self.__class__, self).__init__()

        self.markers = []
        self.enabled = False

        self.font = QtGui.QFont()
        self.font.setPointSize(11)
        self.font.setBold(True)

        self.vbox = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel()
        self.label.setFont(self.font)
        self.label.setText("Autonomous")

        self.button = QtGui.QPushButton()
        self.button.setFont(self.font)
        self.button.setText("Disabled")
        self.button.clicked.connect(self.pressed)

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)

        self.setLayout(self.vbox)

    def pressed(self, e):

        if self.enabled:
            self.enabled = False
            self.button.setText("Disabled")
            # Stop sending auto over udp, keep tcp closed
            self.enableAutoTrigger.emit(False, False)
        else:
            self.enabled = True
            self.requestMarkers.emit()
            self.button.setText("Enabled")
            self.send_data()

    def send_data(self):
        # Set comms to send true, set it to open connection
        self.enableAutoTrigger.emit(True, True)

        for i in range(0, len(self.markers)):

            lat = float(self.markers[i][0])
            lng = float(self.markers[i][1])

            if i == len(self.markers) - 1:
                self.sendData.emit(False, lat, lng)
            else:
                self.sendData.emit(True, lat, lng)

        # Keep sending auto: true over udp but close tcp connection
        self.enableAutoTrigger.emit(True, False)

    def set_markers(self, markers):
        self.markers = markers
