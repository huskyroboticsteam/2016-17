from PyQt4 import QtGui, QtCore
from camera_ptz import PTZCamera
from joystick import Joystick
import sys
import time

max_speed = 100


class CameraMove(QtCore.QThread):
    def __init__(self, js, camera_ip, username, password):
        super(self.__class__, self).__init__()
        self.cam = PTZCamera(camera_ip, username, password)
        self.js = js
        self.x_speed = 0
        self.y_speed = 0

    def run(self):
        while True:
            self.move()
            self.msleep(10)

    def move(self):
        if self.js.ready and self.js.joystick_control[0] is not None:
            hat_val = self.js.joystick_hat[self.js.joystick_control[0]]

            changed = False

            if hat_val == 2:
                if self.x_speed != max_speed:  # Do not combine with if statement above!
                    self.x_speed = max_speed
                    changed = True
            elif hat_val == 8:
                if self.x_speed != -max_speed:
                    self.x_speed = -max_speed
                    changed = True
            elif self.x_speed != 0:
                self.x_speed = 0
                changed = True
            elif hat_val == 1:
                if self.y_speed != max_speed:
                    self.y_speed = max_speed
                    changed = True
            elif hat_val == 4:
                if self.y_speed != -max_speed:
                    self.y_speed = -max_speed
                    changed = True
            elif self.y_speed != 0:
                self.y_speed = 0
                changed = True

            if changed:
                self.cam.set_speeds(self.x_speed, self.y_speed)
        # print "Changed"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    js = Joystick()
    js.start()

    CamMove = CameraMove(js, ["192.168.0.30", "192.168.0.22"], "admin", "1234")
    CamMove.start()

    window = QtGui.QDialog()
    window.show()
    sys.exit(app.exec_())
