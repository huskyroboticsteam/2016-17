from PyQt4 import QtGui, QtCore
from camera_ptz import PTZCamera
from joystick import Joystick
import sys
import time

max_speed = 100

class CameraMove:
	def __init__(self, js, camera_ip, username, password):
		self.cam_instance = PTZCamera(camera_ip, username, password)
		self.js = js
		self.x_speed = 0
		self.y_speed = 0

	def start(self):
		# Ties window refresh to joystick refresh
		#QtGui.QWidget.__init__(self)
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.move_cam)
		self.timer.start(1000 / 100)  # Updates 100 times per second
	
	def move_cam(self):
		hat_val = self.js.joystick_hat  #[0][0] #joystick number, joystick axis
		
		changed = False
		
		if hat_val[0] & 2 == 2:
			if self.x_speed != max_speed: #Do not combine with if statement above!
				self.x_speed = max_speed
				changed = True
		elif hat_val[0] & 8 == 8:
			if self.x_speed != -max_speed:
				self.x_speed = -max_speed
				changed = True
		elif self.x_speed != 0:
			self.x_speed = 0
			changed = True
		elif hat_val[0] & 1 == 1:
			if self.y_speed != max_speed:
				self.y_speed = max_speed
				changed = True
		elif hat_val[0] & 4 == 4:
			if self.y_speed != -max_speed:
				self.y_speed = -max_speed
				changed = True
		elif self.y_speed != 0:
			self.y_speed = 0
			changed = True
		
		if changed:
			self.cam_instance.set_speeds(self.x_speed, self.y_speed)
			#print "Changed"

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	js = Joystick()
	js.start()
	
	CamMove = CameraMove(js, "192.168.0.30", "admin", "1234")
	CamMove.start()
	
	window = QtGui.QDialog()
	window.show()
	sys.exit(app.exec_())