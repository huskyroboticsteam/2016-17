import BNO055
import time
import math

def main():
    bno055 = BNO055.BNO055()
    init_success = bno055.begin()
    if not init_success:
        print 'cannot initialize BNO055'
        return
    with open('calibration_data.txt', 'r') as f:
        bno055.set_calibration(map(int, f.read().split(' ')))
    while True:
        print 'calibration status:', bno055.get_calibration_status()
        print 'euler:', bno055.read_euler()
        magnetometer = bno055.read_magnetometer()
        print 'magnetometer:', magnetometer
        print 'magnetormeter angle:', math.degrees(math.atan2(magnetometer[1], magnetometer[0]))
        time.sleep(0.1)


if __name__ == "__main__":
    main()
