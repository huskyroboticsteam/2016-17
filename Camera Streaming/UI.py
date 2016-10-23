import sys
import CustomWidgets
import Recorder
from PyQt4 import QtGui
import math

sizeX = 520
sizeY = 300


class Player(QtGui.QMainWindow):

    def __init__(self, urls, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Camera Streamer")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.createUI(urls)

    def resizeEvent(self, resizeEvent):
        # print resizeEvent.size()
        for i in range (0, len(self.videos)):
            # print (math.floor(resizeEvent.size().width() / len(self.urls))), (math.floor(resizeEvent.size().width() / len(self.urls)) * 0.5625)
            # if resizeEvent.size().width() > resizeEvent.size().height():
            self.videos[i].resize((math.floor(resizeEvent.size().width() / len(self.urls))), (math.floor(resizeEvent.size().width() / len(self.urls)) * 0.5625))

    def createUI(self, urls):
        self.widget = QtGui.QWidget(self)
        self.widget.setContentsMargins(0, 0, 10, 5)
        self.resize(900, 200)
        self.setCentralWidget(self.widget)

        self.urls = urls

        # Main Horizontal Container
        self.hbox = QtGui.QHBoxLayout()

        # Create the VLC video widgets
        self.videos = createVLCWidgets(urls)

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
        self.widget.setLayout(self.hbox)

        # Give VLC the window to play in then tell it to play the video
        for i in range(0, len(urls)):
            self.videos[i].assignWindowId()
            self.videos[i].play()


def createVLCWidgets(urls):
    # Empty list to hold vlc widgets
    widgets = []

    for i in range(0, len(urls)):
        vlc_widget = CustomWidgets.VLCWidget(urls[i], ":network-caching=300", sizeX, sizeY)
        vlc_widget.id = i
        widgets.append(vlc_widget)

    return widgets

# Main Function
def main(urls, x, y):

    global sizeX
    sizeX = x
    global sizeY
    sizeY = y

    app = QtGui.QApplication(sys.argv)

    # Pass all URL RTSP parameters and random number generator bounds to the UI for initialization
    player = Player(urls)
    player.show()

    # Start the UI loop
    sys.exit(app.exec_())
