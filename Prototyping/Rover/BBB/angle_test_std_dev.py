import BNO055
import time
import math
import Robot


def magnetometer_angle(bno055):
    magnetometer = bno055.read_magnetometer()
    return math.degrees(math.atan2(magnetometer[1], magnetometer[0]))


def standard_deviation(lst, population=True):
    """Calculates the standard deviation for a list of numbers."""
    num_items = len(lst)
    mean = sum(lst) / num_items
    differences = [x - mean for x in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    if population is True:
        variance = ssd / num_items
    else:
        variance = ssd / (num_items - 1)
    return math.sqrt(variance)


def main():
    bno055 = BNO055.BNO055()
    init_success = bno055.begin()
    if not init_success:
        print 'cannot initialize BNO055'
        return
    with open('calibration_data.txt', 'r') as f:
        bno055.set_calibration(map(int, f.read().split(' ')))
    try:
        motor_off_angles = []
        for x in range(100):
            motor_off_angles.append(magnetometer_angle(bno055))
            time.sleep(0.1)
            print x
        rob = Robot.Robot()
        motor_on_angles = []
        for x in range(100):
            for i in range(1, 5):
                rob.driveMotor(i, 200 * (x / 10 % 2))
            motor_on_angles.append(magnetometer_angle(bno055))
            time.sleep(0.1)
            print x
    except KeyboardInterrupt:
        pass
    for i in range(1, 5):
        rob.stopMotor(i)
    print 'motor on std dev:', standard_deviation(motor_on_angles)
    print 'motor off std dev:', standard_deviation(motor_off_angles)


if __name__ == "__main__":
    main()