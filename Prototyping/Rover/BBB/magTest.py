import mag
import Robot
mag = mag.Magnetometer()
rob = Robot.Robot()
while 1:
    print rob.getMag()