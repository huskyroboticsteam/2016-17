from PyQt4 import QtGui
import sys
from ui_components.map import MapWidget
from ui_components.ip_scanner import IPCheckerLayout
from ui_components.camera_streaming import UI

# Link the camera streaming feed when attached over ethernet
camOne = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.20:554/user=admin&password=&channel=1&stream=0.sdp"
camThree = "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"

# Putting all the links into array form
urls = [camOne, camTwo, camThree]

# Specifying the new PyQt4 applicataion and main window
app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()


# Creates the map at 800x200 px and updates at 120 fps
map = MapWidget.MainWindow(800, 200, 120)

# Shows the video streams in their own windows of size 300x200 px
camera = UI.Player(urls, 300, 200)

# Updates IP state every 50 milliseconds. Maps the name to the status.
ip = IPCheckerLayout.IPList({"192.168.1.10": "Rover", "192.168.1.20": "Camera Two"}, 50)

# Make a vertical and horizontal layout
vbox = QtGui.QVBoxLayout()
hbox = QtGui.QHBoxLayout()

# Add the map and IP list to the horizontal layout
hbox.addWidget(map)
hbox.addWidget(ip)
# Add the horizontal layout and camera feed to the vertical layout
vbox.addLayout(hbox)
vbox.addWidget(camera)

# Make the root widget have the nested layout of vbox
wid = QtGui.QWidget()
wid.setLayout(vbox)

# Set main windows root widget and size
window.setCentralWidget(wid)
window.resize(1000, 600)

# Show window, initialize pygame, and execute the app
window.show()
map.initialize()
app.exec_()
