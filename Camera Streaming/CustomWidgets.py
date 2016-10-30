import sys
import vlc
from PyQt4 import QtGui, QtCore


class VLCWidget(QtGui.QFrame):
    def __init__(self, url, options, sizeX, sizeY):
        QtGui.QFrame.__init__(self)

        self.instance = vlc.Instance("--no-audio")

        # Creates the VLC Player Object
        self.player = self.instance.media_player_new()
        self.id = ""
        self.url = url

        self.pal = self.palette()
        self.pal.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.setPalette(self.pal)
        self.setAutoFillBackground(True)

        # Set initial window size of widget
        self.resize(sizeX, sizeY)

        # Set Media that will play
        self.player.set_media(self.instance.media_new(url, options))

    # Need to figure out how events work in PyQT so we can call this function
    # after the widget has been assigned to a layout
    def assignWindowId(self):
        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.player.set_xwindow(self.winId())
        elif sys.platform == "win32":  # for Windows
            self.player.set_hwnd(self.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaplayer.set_nsobject(self.winId())

    def play(self):
        self.player.play()


class Button(QtGui.QPushButton):
    def __init__(self, name, id, recorder):
        QtGui.QPushButton.__init__(self)

        self.setText(name)
        self.recording = False
        self.id = id
        self.recorder = recorder
        self.connect(self, QtCore.SIGNAL("clicked()"), self.record)

    def record(self):
        if not self.recording:
            self.setText("Recording")
            self.recorder.start_recording(self.id)
            self.recording = True
        else:
            self.setText("Record Feed " + str(self.id + 1))
            self.recorder.stop_recording(self.id)
            self.recording = False

