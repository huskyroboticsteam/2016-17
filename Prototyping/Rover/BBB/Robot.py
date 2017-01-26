import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import time

ADC.setup()

# setup i2c to motorshield
pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
pwm.set_pwm_freq(60)

# Potentiometer pin:
POT_PIN = "AIN0"
POT_LEFT = 0.768
POT_MIDDLE = 0.556
POT_RIGHT = 0.331
POT_TOL = 0.001
# 0 if manual 1 if auto drive
auto = 0

'''
ROBOT motor configuration:

Front
+---+
3   4
 \ /
  0
 / \
1   2
+---+
Back

'''



# motor: throttle, F, B
# 1: 8,  9,  10
# 2: 13, 12, 11
# 3: 2,  4,  3
# 4: 7,  6,  5
# drives the motor with a value, negative numbers for reverse
def driveMotor(motor, val):
    # verify value is good
    if abs(val) > 255:
        print "bad value"
        return
    # select proper pins
    if motor == 1:
        throttlePin = 8
        forwardPin = 9
        backPin = 10
    elif motor == 2:
        throttlePin = 13
        forwardPin = 12
        backPin = 11
    elif motor == 3:
        throttlePin = 2
        forwardPin = 4
        backPin = 3
    elif motor == 4:
        throttlePin = 7
        forwardPin = 6
        backPin = 5
    else:
        print "bad motor num"
        return
    pwm.set_pwm(forwardPin, 4096, 0)
    pwm.set_pwm(backPin, 4096, 0)
    pwm.set_pwm(throttlePin,
                2048 + abs((256 - abs(val)) * 8),
                2048 - abs((256 - abs(val)) * 8))
    if val > 0:
        pwm.set_pwm(forwardPin, 0, 4096)
    if val < 0:
        pwm.set_pwm(backPin, 0, 4096)
    print "driving motor: " + str(motor) + " with value: " + str(val)


# returns a float of how far from straight the pot is. > 0 for Right, < 0 for left
def readPot():
    return POT_MIDDLE - ADC.read(POT_PIN)


# returns a tuple of (throttle, turn)
# turn value is 100 for full right -100 for full left and 0 for straight
def getDriveParms(auto):
    return (50, 0)


# returns a tuple of (motor1, motor2, motor3, motor4) from the driveParms modified by the pot reading
def convertParmsToMotorVals(driveParms):
    potReading = readPot()
    result = (driveParms[0] - driveParms[1] + int(potReading * 10),
              driveParms[0] + driveParms[1] - int(potReading * 10),
              driveParms[0] + driveParms[1],
              driveParms[0] - driveParms[1])

    return result


def main():
    try:
        while True:
            driveParms = getDriveParms(auto)
            MotorParms = convertParmsToMotorVals(driveParms)
            for i in range(1, 5):
                driveMotor(i, MotorParms[i - 1])
    except KeyboardInterrupt:
        for i in range(1, 5):
            driveMotor(i, 0)
        print "exiting"


if __name__ == "__main__":
    main()
