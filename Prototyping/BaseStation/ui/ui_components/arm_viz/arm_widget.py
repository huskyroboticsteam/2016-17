from PyQt4 import QtGui, QtCore
import numpy as np
from armature import *
from math import pi


class arm_widget(QtGui.QWidget):
    def __init__(self):
        super(arm_widget, self).__init__()

        draw_origin = np.array([320, 0, 240])
        draw_matrix = tr.translation_matrix(draw_origin)
        # test_armature = make_tentacle(40, 10)
        test_armature = Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(30, Parameter(0, pi / 4), FixedParameter(0),
                        Arm(10, Parameter(0, pi / 4), FixedParameter(0)))))

        params = test_armature.min_parameters()
        target = np.array([0, 0, 0])

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red))
        painter.drawLine(4,4,500,500)