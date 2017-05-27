# For cx_freeze. This allows the DLLs to be loaded from the application directory, 
# rather than the install directory which doesn't always exist
import os
if "PYSDL2_DLL_PATH" not in os.environ:
    os.environ["PYSDL2_DLL_PATH"] = "."

from PyQt4 import QtGui, uic
import sys
from ui_components.map import Map
from ui_components.ip_scanner import IPCheckerLayout
from ui_components.camera_streaming import UI
from ui_components.emergency_stop import stop
from ui_components.settings import settings
from ui_components import comms_update, joystick, Camera_Controller
from ui_components.arm_viz import arm_widget
from ui_components.sensors import SensorChecker
from ui_components.list_widget import list_widget
from ui_components.auto_indicator import auto


def quitting():
    # Close all connection threads
    sock.shutdown()
    # Shutdown the networking thread
    iplist.worker.quit()
    # Save the changes to the settings by the user
    setting_widget.save()

    cam1.quit()
    cam2.quit()

# Specifying the new PyQt4 applicataion and main window
app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('rocket-icon.png'))

# Call this function when we are about to quit
app.aboutToQuit.connect(quitting)
win = QtGui.QMainWindow()

# Load the UI into the main window
main = uic.loadUi("ui.ui", win)
win.setWindowTitle("Husky Robotics Control GUI")

win.resize(1200, 675)

'''Init the Joysticks and Camera Movement Code'''
joys = joystick.getJoysticks()
joys.start()
cam1 = Camera_Controller.CameraMove(joys, "192.168.0.30", "admin", "1234")
cam1.start()
cam2 = Camera_Controller.CameraMove(joys, "192.168.0.22", "admin", "1234")
cam2.start()

'''Create all the custom widgets for the UI'''
sensors = SensorChecker.SensorData()
sock = comms_update.ConnectionManager()
setting_widget = settings.Settings(main)
stop_widget = stop.Stop()

vlc_widget = UI.Player(setting_widget.get_camera_urls(), 300, 200)
# IP Pinging List, update specified in milliseconds
iplist = IPCheckerLayout.IPList({"192.168.0.50": "Rover Main", "192.168.0.90": "Arm Main", "192.168.0.91":
                                "Science Main", "192.168.0.22": "Eye of Sauron", "192.168.0.42": "Ground Cam",
                                 "192.168.0.15": "Arm Cam"}, 500)
arm = arm_widget.arm_widget()
list_wid = list_widget.ListWidget()
map = Map.Map(setting_widget.get_map_name())
auto_button = auto.Auto()

'''Add all the custom widgets to the UI containers'''
# Create the emergency stop button
main.stop_container.addWidget(stop_widget)
# Shows the video streams in their own windows of size 300x200 px
main.camera_container.addWidget(vlc_widget)
# Updates IP state every 50 milliseconds. Maps the name to the status.
main.sensor_container.addWidget(iplist)
# Add the arm visualization
main.joystick_container.addWidget(arm)
# Add the sensor reading widget
main.reading_container.addWidget(sensors)
# Add the map to the ui
main.map_container.addWidget(map)
# Add the marker list view to the ui
main.list_container.addWidget(list_wid)
# Add the label that indicates autonomous mode to the ui
main.list_container.addWidget(auto_button)

'''Connect all events for each of the components to talk to one another'''
auto_button.enableAutoTrigger.connect(sock.enable_tcp)
sock.auto.tcp_enabled.connect(sock.drive.enable_tcp)
sock.auto.tcp_enabled.connect(auto_button.set_enabled)
sock.auto.requestMarkers.connect(list_wid.get_markers)
list_wid.giveMarkers.connect(sock.auto.set_markers)

# Tell the science station to take a picture
sensors.picture_signal.connect(sock.science.send_picture)
sensors.slider_signal.connect(sock.science.send_sliders)

sock.drive.sensorUpdate.connect(sensors.update_ui)
sock.science.sensorUpdate.connect(sensors.update_ui)
sock.drive.gpsUpdate.connect(map.update_rover_pos)


map.signal.connect(list_wid.add_to_ui)
map.updateList.connect(list_wid.update_from_ui)
stop_widget.stopEvent.connect(sock.drive.stopping)
list_wid.callToDelete.connect(map.remove_marker)
list_wid.highlightMarker.connect(map.highlight_marker)
list_wid.replaceMarker.connect(map.replace_marker)


# Show window and execute the app
win.show()

sys.exit(app.exec_())
