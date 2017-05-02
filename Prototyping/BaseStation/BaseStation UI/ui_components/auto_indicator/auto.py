from PyQt4 import QtGui, QtCore


class Auto(QtGui.QWidget):
    """
        A simple widget that displays the text "AUTO" or displays nothing
    """

    # Expects auto comms status, connection open?
    enableAutoTrigger = QtCore.pyqtSignal(bool)

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
        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.button.setSizePolicy(policy)
        self.button.setFont(self.font)
        self.button.setText("Disabled")
        self.button.clicked.connect(self.pressed)

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)

        self.setLayout(self.vbox)

    def pressed(self):

        if self.enabled:
            self.enabled = False
            self.button.setText("Disabled")
            # Stop sending auto over udp, keep tcp closed
            self.enableAutoTrigger.emit(False)
        else:
            self.enabled = True
            self.button.setText("Enabled")
            self.enableAutoTrigger.emit(True)

    def set_markers(self, markers):
        self.markers = markers
