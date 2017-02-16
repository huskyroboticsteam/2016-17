from PyQt4 import QtGui, QtCore
import numpy as np
from armature import *
from math import pi
from gradient_descent import *

"""
Visualizes the arm using computations in 3d space mapped to a 2d surface
Currently follows a target that is moved by mouse input but eventually will use real arm data
"""

class arm_widget(QtGui.QWidget):
    def __init__(self):
        super(arm_widget, self).__init__()

        # Initialize the origin of all drawing to the top left of the screen
        self.draw_origin = np.array([0, 0, 0])

        # Make a new 3d armature with lengths proportional to real arm
        self.test_armature = Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(50, Parameter(0, pi), FixedParameter(0),
                        Arm(30, Parameter(0, pi / 4), FixedParameter(0),
                        Arm(10, Parameter(0, pi / 4), FixedParameter(0)))))

        # Make the starting params for the arm
        self.params = self.test_armature.min_parameters()

        # Where the arm will be pointing at
        self.target = np.array([0, 0, 0])

        # Pen to draw to the screen
        self.pen = QtGui.QPen(QtCore.Qt.gray)
        self.pen.setWidth(8)

    # We wait until the window is about to show before we initialize real draw origin
    def showEvent(self, e):
        self.resize_self()

    # Recalculate width and height of the window if we resize
    # Overrides parent class method but calls super so children resize properly
    def resizeEvent(self, QResizeEvent):
        super(arm_widget, self).resizeEvent(QResizeEvent)
        self.resize_self()

    # Overrides parent class method, called every time we move the mouse with left button down in window
    def mouseMoveEvent(self, e):
        # Get mouse x and y in the window
        x = e.x()
        y = e.y()

        # Update the mouse position to the drawn coord system
        arr = np.array([x, 0, y]) - np.array([self.width() / 2, 0, self.height() / 1.1])

        # If we are within 40 pixels of the target we can move it
        if distance(arr, self.target) < 40:
            # Make the target the mouse draw position
            self.target = arr
            # Recalculate the arm positioning
            self.params = gradient_descent(self.test_armature, self.params, self.target, 10)
            # Redraw the window since we updated
            self.repaint()

    def paintEvent(self, QPaintEvent):

        # Object that paints to the screen
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)

        # Set pen color to red for the target
        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(5)
        painter.setPen(self.pen)
        # Draw the target at the target x, y position offset by drawing origin
        painter.drawEllipse(QtCore.QPointF(self.target[::2][0] + self.draw_origin[::2][1],
                                           self.target[::2][1] + self.draw_origin[::2][0]), 10, 10)
        # Se pen color to gray
        self.pen.setColor(QtCore.Qt.gray)
        self.pen.setWidth(8)
        painter.setPen(self.pen)

        # Get the points where the arm joints are located
        unf_points = [point[::2] for point in self.test_armature.joints(self.params)]
        points = []

        # Make all numerical points QPointF objects offset by draw origin
        for i in range(0, len(unf_points)):
            points.append(QtCore.QPointF(unf_points[i][0], unf_points[i][1]))
            points[i].setX(points[i].x() + self.draw_origin[::2][1])
            points[i].setY(points[i].y() + self.draw_origin[::2][0])

        # Make every segment a different color, draw lines with the points
        for i in range(1, len(points)):
            self.flip_color(painter)
            painter.drawLine(points[i-1], points[i])

    # Toggle the pen color
    def flip_color(self, painter):
        if self.pen.color() == QtCore.Qt.gray:
            self.pen.setColor(QtCore.Qt.black)
            painter.setPen(self.pen)
        else:
            self.pen.setColor(QtCore.Qt.gray)
            painter.setPen(self.pen)

    # Recalculate the draw origin if the window is resized
    def resize_self(self):
        self.draw_origin = np.array([self.height() / 1.1, 0, self.width() / 2])

