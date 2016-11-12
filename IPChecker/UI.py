import socket
from PyQt4 import QtGui, QtCore
import sys
import threading


class myThread (threading.Thread):
    def __init__(self, result, path):
        threading.Thread.__init__(self)
        self.result = result
        self.path = path
    def run(self):
        # Get lock to synchronize threads
        # self.lock.acquire()
        self.result.append((self.ping(self.path), self.path, int(self.path.split(".")[3])))
        # Free lock to release next thread
        # self.lock.release()

    def ping(self, host):
        """
        Returns True if host responds to a ping request
        """
        import os, platform

        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        # Ping
        return os.system("ping " + ping_str + " " + host) == 0


class MainUI(QtGui.QMainWindow):
    def __init__(self, lower, upper, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("IP Scanner")
        # self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.lower = lower
        self.upper = upper

        self.myIP = str(socket.gethostbyname(socket.gethostname()))

        ipseg = self.myIP.split(".")
        self.path = ""
        for i in range(0, len(ipseg) - 1):
            self.path += ipseg[i] + "."

        self.create_ui()

    def create_ui(self):

        self.build_initial_ui()

        # Add all layouts to main container
        self.widget.setLayout(self.build_list(self.threaded_ping()))

        # Refresh the IP list every 20 seconds
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_ui)
        timer.start(20000)

    def build_initial_ui(self):
        self.widget = QtGui.QWidget(self)
        self.widget.setContentsMargins(20, 0, -20, 0)
        self.resize(300, 50)
        self.setCentralWidget(self.widget)

    def update_ui(self):
        list = self.build_list(self.threaded_ping())
        self.widget.destroy(True, True)
        self.build_initial_ui()
        self.widget.setLayout(list)

    def threaded_ping(self):
        # threadLock = threading.Lock()
        threads = []
        results = []

        for i in range(self.lower, self.upper + 1):
            thread = myThread(results, (self.path + str(i)))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()

        return sorted(results, key=lambda ip: ip[2])

    def build_list(self, results):
        vbox = QtGui.QVBoxLayout()
        for i in range(0, len(results)):
            if results[i][0]:
                hbox = QtGui.QHBoxLayout()
                label = QtGui.QLabel()
                label.setText(results[i][1])
                label2 = QtGui.QLabel()
                label2.setText("Active")
                hbox.addWidget(label)
                hbox.addWidget(label2)
                vbox.addLayout(hbox)

        return vbox


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    # UI updates every 20 seconds, given upper and lower bounds of IPs to scan over
    ui = MainUI(1, 200)
    ui.show()

    # Start the UI loop
    sys.exit(app.exec_())