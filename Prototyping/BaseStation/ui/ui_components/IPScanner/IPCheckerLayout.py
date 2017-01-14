import NetworkChecker
from PyQt4 import QtGui, QtCore
import PingThread


class IPList(QtGui.QWidget):
    def __init__(self, ip_map, update_time, parent=None):
        super(IPList, self).__init__(parent)

        NetworkChecker.check_network(ip_map)

        self.map = ip_map

        # Populated with keys from self.map to the QtLabel objects indicating activity
        self.ui_map = {}

        self.setLayout(self.build_list())
        self.update_ui()

        # Refresh the IP list every given time
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui)
        timer.start(update_time)

    def update_ui(self):
        results = self.threaded_ping()
        # print results
        for i in range(0, len(results)):
            if results[i][1]:
                self.ui_map[results[i][0]].setText("Active")
            else:
                self.ui_map[results[i][0]].setText("Fail")

    def threaded_ping(self):
        threads = []
        results = []

        for key, value in self.map.iteritems():
            thread = PingThread.MyThread(results, key)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        return results

    def build_list(self):
        vbox = QtGui.QVBoxLayout()
        for key, value in self.map.iteritems():
            hbox = QtGui.QHBoxLayout()

            label = QtGui.QLabel()
            label.setText(value)
            label2 = QtGui.QLabel()

            label2.setText("Active")

            hbox.addWidget(label)
            hbox.addWidget(label2)
            vbox.addLayout(hbox)

            self.ui_map[key] = label2

        return vbox
