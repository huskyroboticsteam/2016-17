import NetworkChecker
from PyQt4 import QtGui, QtCore
import subprocess, os

"""
Internally checks a give list of ips for status.
Indicates visually with a red or green light whether the ip is active or not.
Will warn the user if the local machine is not on the same network as the rover.
"""


class IPList(QtGui.QWidget):
    def __init__(self, ip_map, update_time, parent=None):
        super(IPList, self).__init__(parent)

        NetworkChecker.check_network(ip_map)

        self.map = ip_map

        # Populated with ips from self.map to the QWidget objects indicating activity
        self.ui_map = {}

        self.setLayout(self.build_list())

        # Operate the updates on a new separate thread so we don't block the UI thread
        self.worker = MyThread(self.map)
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)

        # Start the thread; is stopped when the application closes
        self.worker_thread.start()

        # If the thread emits on signalStatus run the update ui method
        self.worker.signalStatus.connect(self.update_ui)

        # Refresh the IP list every given time
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.worker.start_work)
        timer.start(update_time)

    def update_ui(self, results):
        for i in range(0, len(results)):
            # Get the QWidget indicator object by ip
            indicator = self.ui_map[results[i][0]]
            if results[i][1]:
                # If the result boolean is True set the background color to green
                p = indicator.palette()
                color = QtGui.QColor()
                color.setRgb(0, 255, 0, 255)
                p.setColor(indicator.backgroundRole(), color)
                p.setColor(indicator.foregroundRole(), color)
                indicator.setPalette(p)
            else:
                # If the result boolean is False set the background color to red
                p = indicator.palette()
                color = QtGui.QColor()
                color.setRgb(255, 0, 0, 255)
                p.setColor(indicator.backgroundRole(), color)
                p.setColor(indicator.foregroundRole(), color)
                indicator.setPalette(p)

    def build_list(self):
        # Vertically holds the list of friendly names for the ips and indicators
        vbox = QtGui.QVBoxLayout()
        for key, value in self.map.iteritems():
            # Holds a single name and indicator pair
            hbox = QtGui.QHBoxLayout()

            # Indicator widget
            indicator = QtGui.QWidget()
            indicator.setFixedSize(10, 10)
            indicator.setAutoFillBackground(True)

            # Set default coloration to purple (for testing if updates work)
            p = indicator.palette()
            color = QtGui.QColor()
            color.setRgb(145, 44, 238, 255)
            p.setColor(indicator.backgroundRole(), color)
            indicator.setPalette(p)

            # Friendly name for the ip
            label = QtGui.QLabel()
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.setText(value)

            # Indicator on the left, label on the right
            hbox.addWidget(indicator)
            hbox.addWidget(label)

            vbox.addLayout(hbox)

            # Map the ip to the indicator object so we can update it later
            self.ui_map[key] = indicator

        # Force all hboxes to align to the top
        vbox.setAlignment(QtCore.Qt.AlignTop)

        return vbox


class MyThread(QtCore.QObject):

    # A new signal that transmits a list object
    # Communicates through PyQt to the UI thread
    signalStatus = QtCore.pyqtSignal([list])

    # Takes in the ips we want to check
    def __init__(self, paths):
        super(MyThread, self).__init__()
        self.paths = paths

    def start_work(self):
        results = []

        # Ping all ips in the list
        for key, value in self.paths.iteritems():
            results.append((key, self.ping(key)))

        # Tell PyQt the work is done and send the results to listeners
        # Results list is contains tuples of (ip, isActive boolean)
        self.signalStatus.emit(results)

    # Ping the remote host
    def ping(self, hostname):
        """ Use the ping utility to attempt to reach the host. We send 5 packets
        ('-c 5') and wait 3 milliseconds ('-W 3') for a response. The function
        returns the return code from the ping utility.
        Works on all operating systems.
        """

        ret_code = subprocess.call(['ping', '-c', '5', '-W', '3', hostname],
                                   stdout=open(os.devnull, 'w'),
                                   stderr=open(os.devnull, 'w'))
        return ret_code == 0
