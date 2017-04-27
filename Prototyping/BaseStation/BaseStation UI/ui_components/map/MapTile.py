from PyQt4 import QtGui
import os


class MapTile:
    def __init__(self, path, file_name, x, y):
        # Image dimensions will be static and handled by the map class

        # Image for the tile
        self.image = QtGui.QImage(os.path.join(path, file_name))

        # Top left corner of the image
        self.screen_location = (x, y)

        # Whether the image is visible on screen
        self.visible = False

    # Update the location on screen when moving
    def move(self, dx, dy):

        """
        Move the tile by a given dx and dy
        :param dx: The number of pixels on the x-axis to move the tile (up is positive)
        :param dy: The number of pixels on the y-axis to move the tile (right is positive)
        :return: None
        """

        self.screen_location = (self.screen_location[0] + dx, self.screen_location[1] + dy)