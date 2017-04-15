from PyQt4 import QtGui, QtCore

class Marker:

    def __init__(self, x, y, centerX, centerY, zoom_level, lat, long, color=QtCore.Qt.gray):
        """
        A flexible marker that can be placed on the map by a user
        :param x (float): The x position of this marker on the display
        :param y (float): The y position of this marker on the display
        :param centerX (float): The shift of x coordinate of the map relative to the display screen
        :param centerY (float): The shift of y coordinate of the map relative to the display screen
        :param zoom_level (int): The current zoom level of map
        :param lat (float): Original latitude entered of marker
        :param long (float): Original longitude entered of marker
        :param rover (boolean): Is the marker the rover
        :param color (QtCore color): default = gray unless specified
        """

        self.x = x
        self.y = y
        self.centerX = centerX
        self.centerY = centerY
        self.zoom_level = zoom_level
        self.coordX = lat
        self.coordY = long
        self.pen = QtGui.QPen(color)

    def draw(self, painter):
        """
        :param painter (PyQt4):

        Draws a marker onto map.
        Blue marker if it is rover, red for other markers
        """
        self.pen.setWidth(5)
        painter.setPen(self.pen)
        painter.drawEllipse(int(self.x) - self.centerX - 10, int(self.y) - self.centerY - 10, 20, 20)

    def set_color(self, color):
        self.pen = QtGui.QPen(color)