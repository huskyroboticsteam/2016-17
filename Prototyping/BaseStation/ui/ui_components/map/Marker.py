class Marker:

    def __init__(self, x, y, centerX, centerY, zoom_level, long, lat, rover):
        self.x = x
        self.y = y
        self.centerX = centerX
        self.centerY = centerY
        self.zoom_level = zoom_level
        self.coordX = long
        self.coordY = lat
        self.rover = rover

    def draw(self, painter):
        if self.rover:
            painter.drawEllipse(int(self.x) - self.centerX, int(self.y) - self.centerY, 20, 20)
        else:
            painter.drawEllipse(int(self.x) - self.centerX, int(self.y) - self.centerY, 20, 20)