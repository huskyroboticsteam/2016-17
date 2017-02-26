from PyQt4 import QtGui
import sys
from ui_components.map import Map
from ui_components.ip_scanner import IPCheckerLayout
from ui_components.camera_streaming import UI
from ui_components.emergency_stop import stop
from ui_components.settings import settings
from ui_components import Command, comms_update
from ui_components.arm_viz import arm_widget
from ui_components.sensors import SensorChecker
from ui_components.list_widget import list_widget
from ui_components.auto_indicator import auto
from ui import Ui_MainWindow


def quitting():
    # Close all open sockets
    sock.shutdown()
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
sensors = SensorChecker.SensorData()
#comm = command_api.CommandApi(sensors)
sock = comms_update.CommsUpdate()
setting_widget = settings.Settings(main)

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

main.reading_container.addWidget(sensors)

# Show window, initialize pygame, and execute the app
win.show()

map = Map.Map(setting_widget.get_map_name())
main.map_container.addWidget(map)
list_wid = list_widget.ListWidget(map)
command_line = Command.command(map, sock, list_wid)
command_line.signalStatus.connect(sock.send_auto_mode)
list_wid.signalStatus.connect(command_line.update)
sock.signalStatus.connect(sensors.update_ui)
sock.signalUpdate.connect(map.update_rover_pos)
main.map_container.addWidget(command_line)
main.list_container.addWidget(list_wid)
auto_lab = auto.Auto()
command_line.autoTrigger.connect(auto_lab.toggle_ui)

main.list_container.addWidget(auto_lab)

# Creates the map at 800x200 px and updates at 30 fps

map.signal.connect(list_wid.add_to_ui)
map.removeSignal.connect(list_wid.remove_from_ui)



sys.exit(app.exec_())
