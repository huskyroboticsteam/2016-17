from PyQt4 import QtGui, QtCore
import numpy as np
from armature import *
from math import pi
from gradient_descent import *


class arm_widget(QtGui.QWidget):
    def __init__(self):
        super(arm_widget, self).__init__()

        self.draw_origin = np.array([0, 0, 0])
        self.test_armature = Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(30, Parameter(0, pi / 4), FixedParameter(0),
                        Arm(10, Parameter(0, pi / 4), FixedParameter(0)))))

        self.params = self.test_armature.min_parameters()
        self.target = np.array([0, 0, 0])

        self.pen = QtGui.QPen(QtCore.Qt.gray)
        self.pen.setWidth(8)

    # We have to wait until the window is show before we initialize window width and height
    def showEvent(self, e):
        self.resize_self()

    # Recalculate width and height if we resize
    def resizeEvent(self, QResizeEvent):
        super(arm_widget, self).resizeEvent(QResizeEvent)
        self.resize_self()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        arr = np.array([x, 0, y]) - np.array([self.width() / 2, 0, self.height() / 1.1])

        if distance(arr, self.target) < 40:
            self.target = arr
            self.params = gradient_descent(self.test_armature, self.params, self.target, 10)
            self.repaint()

    def paintEvent(self, QPaintEvent):

        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)

        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(5)
        painter.setPen(self.pen)
        painter.drawEllipse(QtCore.QPointF(self.target[::2][0] + self.draw_origin[::2][1],
                                           self.target[::2][1] + self.draw_origin[::2][0]), 10, 10)
        self.pen.setColor(QtCore.Qt.gray)
        self.pen.setWidth(8)
        painter.setPen(self.pen)

        unf_points = [point[::2] for point in self.test_armature.joints(self.params)]
        points = []

        for i in range(0, len(unf_points)):
            points.append(QtCore.QPointF(unf_points[i][0], unf_points[i][1]))
            points[i].setX(points[i].x() + self.draw_origin[::2][1])
            points[i].setY(points[i].y() + self.draw_origin[::2][0])

        for i in range(1, len(points)):
            self.flip_color(painter)
            painter.drawLine(points[i-1], points[i])

    def flip_color(self, painter):
        if self.pen.color() == QtCore.Qt.gray:
            self.pen.setColor(QtCore.Qt.black)
            painter.setPen(self.pen)
        else:
            self.pen.setColor(QtCore.Qt.gray)
            painter.setPen(self.pen)

    def resize_self(self):
        self.draw_origin = np.array([self.height() / 1.1, 0, self.width() / 2])

