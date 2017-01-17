import CustomWidgets
import Recorder
from PyQt4 import QtGui
import math

class Player(QtGui.QWidget):

    def __init__(self, urls, x, y, master=None):
        super(Player, self).__init__(master)
        self.sizeX = x
        self.sizeY = y
        self.createUI(urls)

    def resizeEvent(self, resizeEvent):
        # print resizeEvent.size()
        for i in range (0, len(self.videos)):
            # print (math.floor(resizeEvent.size().width() / len(self.urls))), (math.floor(resizeEvent.size().width() / len(self.urls)) * 0.5625)
            # if resizeEvent.size().width() > resizeEvent.size().height():
            self.videos[i].resize((math.floor(resizeEvent.size().width() / len(self.urls))), (math.floor(resizeEvent.size().width() / len(self.urls)) * 0.5625))

    def createUI(self, urls):
        self.widget = QtGui.QWidget(self)
        self.setContentsMargins(0, 0, 10, 5)

        self.urls = urls

        # Main Horizontal Container
        self.hbox = QtGui.QHBoxLayout()

        # Create the VLC video widgets
        self.videos = self.createVLCWidgets(urls)

        self.recorder = Recorder.VLCRecorder(urls)

        for i in range(0, len(urls)):
            # Vertical box will hold the video and its corresponding record button
            vbox = QtGui.QVBoxLayout()

            label = QtGui.QLabel()
            label.setFixedHeight(15)
            label.setText("URL: " + urls[i])

            vbox.addWidget(label)

            # Add video widget to layout container
            vbox.addWidget(self.videos[i])

            # Create record button then add to layout container
            recordButton = CustomWidgets.Button("Record Feed " + str(self.videos[i].id + 1), self.videos[i].id, self.recorder)
            vbox.addWidget(recordButton)

            # Add all vertical layout containers to a horizontal container
            self.hbox.addLayout(vbox)

        # Add all layouts to main container
        self.setLayout(self.hbox)

        # Give VLC the window to play in then tell it to play the video
        for i in range(0, len(urls)):
            self.videos[i].assignWindowId()
            self.videos[i].play()

    def createVLCWidgets(self, urls):
        # Empty list to hold vlc widgets
        widgets = []

        for i in range(0, len(urls)):
            vlc_widget = CustomWidgets.VLCWidget(urls[i], ":network-caching=300", self.sizeX, self.sizeY)
            vlc_widget.id = i
            widgets.append(vlc_widget)

        return widgets
