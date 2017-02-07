import NetworkChecker
from PyQt4 import QtGui, QtCore
import subprocess, os


class IPList(QtGui.QWidget):
    def __init__(self, ip_map, update_time, parent=None):
        super(IPList, self).__init__(parent)

        NetworkChecker.check_network(ip_map)

        self.map = ip_map

        # Populated with keys from self.map to the QtLabel objects indicating activity
        self.ui_map = {}

        self.setLayout(self.build_list())

        # Operate the updates on the thread
        self.worker = MyThread(self.map)
        self.worker_thread = QtCore.QThread()
        self.worker.moveToThread(self.worker_thread)

        # Thread is stopped when the application closes
        self.worker_thread.start()

        self.worker.signalStatus.connect(self.update_ui)

        # Refresh the IP list every given time
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.worker.start_work)
        timer.start(update_time)

    def update_ui(self, results):
        # print results
        for i in range(0, len(results)):
            val = self.ui_map[results[i][0]]
            if results[i][1]:
                p = val.palette()
                color = QtGui.QColor()
                color.setRgb(0, 255, 0, 255)
                p.setColor(val.backgroundRole(), color)
                p.setColor(val.foregroundRole(), color)
                self.ui_map[results[i][0]].setPalette(p)
            else:
                p = val.palette()
                color = QtGui.QColor()
                color.setRgb(255, 0, 0, 255)
                p.setColor(val.backgroundRole(), color)
                p.setColor(val.foregroundRole(), color)
                val.setPalette(p)

    def build_list(self):
        vbox = QtGui.QVBoxLayout()
        for key, value in self.map.iteritems():
            hbox = QtGui.QHBoxLayout()

            indicator = QtGui.QWidget()
            indicator.setFixedSize(10, 10)
            indicator.setAutoFillBackground(True)

            # Set default coloration
            p = indicator.palette()
            color = QtGui.QColor()
            color.setRgb(145, 44, 238, 255)
            p.setColor(indicator.backgroundRole(), color)
            # p.setColor(self.foregroundRole(), color)
            indicator.setPalette(p)

            label = QtGui.QLabel()
            label.setAlignment(QtCore.Qt.AlignLeft)
            label.setText(value)

            hbox.addWidget(indicator)
            hbox.addWidget(label)

            vbox.addLayout(hbox)

            self.ui_map[key] = indicator

        vbox.setAlignment(QtCore.Qt.AlignTop)

        return vbox


class MyThread(QtCore.QObject):

    signalStatus = QtCore.pyqtSignal([list])

    def __init__(self, paths):
        super(MyThread, self).__init__()
        self.paths = paths

    def start_work(self):
        results = []

        for key, value in self.paths.iteritems():
            results.append((key, self.ping(key)))

        self.signalStatus.emit(results)

    def ping(self, hostname):
        """ Use the ping utility to attempt to reach the host. We send 5 packets
        ('-c 5') and wait 3 milliseconds ('-W 3') for a response. The function
        returns the return code from the ping utility.
        """

        ret_code = subprocess.call(['ping', '-c', '5', '-W', '3', hostname],
                                   stdout=open(os.devnull, 'w'),
                                   stderr=open(os.devnull, 'w'))
        return ret_code == 0
