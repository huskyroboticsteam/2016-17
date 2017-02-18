from PyQt4 import QtGui
import sys
from ui_components.map import MapWidget
from ui_components.ip_scanner import IPCheckerLayout
from ui_components.camera_streaming import UI
from ui_components.emergency_stop import stop
from ui_components.settings import settings
from ui_components import command_api, Command, comms_update
from ui_components.arm_viz import arm_widget
from ui_components.sensors import SensorChecker
from ui import Ui_MainWindow


def quitting():
    # Properly shutdown the pygame window
    internal_map.close()
    # Shutdown the networking thread
    iplist.worker_thread.quit()
    # Save the changes to the settings by the user
    setting_widget.save()


# Specifying the new PyQt4 applicataion and main window
app = QtGui.QApplication(sys.argv)
# Call this function when we are about to quit
app.aboutToQuit.connect(quitting)
win = QtGui.QMainWindow()
main = Ui_MainWindow()
main.setupUi(win)
win.resize(1200, 675)
comm = command_api.CommandApi(SensorChecker)
sock = comms_update.CommsUpdate(comm)
setting_widget = settings.Settings(main, comm)

# Creates the map at 800x200 px and updates at 30 fps
map = MapWidget.MainWindow(600, 200, 30)
main.map_container.addWidget(map)

# Create the emergency stop button
main.stop_container.addWidget(stop.Stop())

# Shows the video streams in their own windows of size 300x200 px
print setting_widget.get_camera_urls()
main.camera_container.addWidget(UI.Player(setting_widget.get_camera_urls(), 300, 200))

iplist = IPCheckerLayout.IPList({"192.168.1.10": "Rover", "192.168.1.20": "Camera Two"}, 50)
# Updates IP state every 50 milliseconds. Maps the name to the status.
main.sensor_container.addWidget(iplist)

# Add the arm visualization
main.joystick_container.addWidget(arm_widget.arm_widget())

main.reading_container.addWidget(SensorChecker.SensorData())

# Show window, initialize pygame, and execute the app
win.show()

internal_map = map.initialize(setting_widget.get_map_name())
command_line = Command.command(internal_map.m, sock)
main.map_container.addWidget(command_line)

# Give the command api the map to talk to
comm.feedin_map(internal_map.m)


sys.exit(app.exec_())
