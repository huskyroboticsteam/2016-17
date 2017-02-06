from PyQt4 import QtGui
import sys
from ui_components.map import MapWidget, Command
from ui_components.ip_scanner import IPCheckerLayout
from ui_components.camera_streaming import UI
from ui_components.emergency_stop import stop
from ui_components.settings import settings
from ui_components import command_api
from ui import Ui_MainWindow


def quitting():
    setting_widget.save()

# Link the camera streaming feed when attached over ethernet
camOne = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.20:554/user=admin&password=&channel=1&stream=0.sdp"
camThree = "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"

# Putting all the links into array form
urls = [camOne, camTwo, camThree]

# Specifying the new PyQt4 applicataion and main window
app = QtGui.QApplication(sys.argv)
app.aboutToQuit.connect(quitting)
win = QtGui.QMainWindow()
main = Ui_MainWindow()
main.setupUi(win)

# Creates the map at 800x200 px and updates at 120 fps
map = MapWidget.MainWindow(600, 200, 120)
main.map_container.addWidget(map)

# Create the emergency stop button
main.stop_container.addWidget(stop.Stop())

# Shows the video streams in their own windows of size 300x200 px
main.camera_container.addWidget(UI.Player(urls, 300, 200))

# Updates IP state every 50 milliseconds. Maps the name to the status.
main.sensor_container.addWidget(IPCheckerLayout.IPList({"192.168.1.10": "Rover", "192.168.1.20": "Camera Two"}, 50))

comm = command_api.CommandApi()
setting_widget = settings.Settings(main, comm)

# Show window, initialize pygame, and execute the app
win.show()
internal_map = map.initialize(setting_widget.get_map_name())

command_line = Command.command(internal_map)
main.map_container.addWidget(command_line)

# Give the command api the map to talk to
comm.feedin_map(internal_map.m)
sys.exit(app.exec_())
