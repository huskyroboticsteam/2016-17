from PyQt4 import QtGui, QtCore


class Auto(QtGui.QLabel):
    """
        A simple widget that displays the text "AUTO" or displays nothing
    """

    def __init__(self):
        super(self.__class__, self).__init__()

        # Initial text is blank
        self.setText("")

        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def toggle_ui(self, on):
        """
        Toggles the text between "AUTO" and ""
        :param on: Boolean - current state of the object display
        :return: None
        """
        if on:
            self.setText("")
        else:
            self.setText("AUTO")
