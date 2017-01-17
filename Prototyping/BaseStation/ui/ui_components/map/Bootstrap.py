from PyQt4 import QtGui, QtCore
import os
import PygameWrapper


class ImageWidget(QtGui.QFrame):
    def __init__(self, width, height, fps):
        QtGui.QFrame.__init__(self)

        self.resize(width, height)
        self.fps = fps
        self.update_func = None
        self.wid = None
        self.data = ""

    def start_updates(self):
        if self.update_func is None:
            print("Main loop undefined")
        else:
            timer = QtCore.QTimer(self)
            timer.timeout.connect(self.update_func)
            #timer.timeout.connect(self.update_data)
            timer.start(1000 / self.fps)

    def update_data(self):
      self.data = self.wid.data

def bootstrap_pygame(frame):
    # Set the variable to show PyGame where to place its window
    os.environ['SDL_WINDOWID'] = str(int(frame.winId()))

    wid = PygameWrapper.PygameWrapper(frame.width(), frame.height())
    frame.wid = wid

    # Set the PyGame update loop be handled by PyQt4
    frame.update_func = wid.main_loop
    frame.start_updates()