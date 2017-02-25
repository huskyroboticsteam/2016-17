import BNO055
import time
import math
import Robot

def main():
    bno055 = BNO055.BNO055()
    init_success = bno055.begin()
    if not init_success:
        print 'cannot initialize BNO055'
        return
    with open('calibration_data.txt', 'r') as f:
        bno055.set_calibration(map(int, f.read().split(' ')))
    rob = Robot.Robot()
    for i in range(1, 5):
        rob.driveMotor(i, 200)
    try:
        while True:
            print 'calibration status:', bno055.get_calibration_status()
            print 'euler:', bno055.read_euler()
            magnetometer = bno055.read_magnetometer()
            print 'magnetometer:', magnetometer
            print 'magnetometer angle:', math.degrees(math.atan2(magnetometer[1], magnetometer[0]))
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    for i in range(1, 5):
        rob.stopMotor(i)


if __name__ == "__main__":
    main()
