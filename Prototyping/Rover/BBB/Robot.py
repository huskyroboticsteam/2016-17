import Adafruit_BBIO.ADC as ADC
import Adafruit_PCA9685
import time
import PID
import math


ADC.setup()

# setup i2c to motorshield
pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
pwm.set_pwm_freq(60)

# Potentiometer pin:
POT_PIN = "AIN2"
POT_LEFT = 0.566
POT_MIDDLE = 0.447
POT_RIGHT = 0.287
POT_TOL = 0.01
# 0 if manual 1 if auto drive
auto = 0

pot_pid = PID.PID(-1,0,0)

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
    val = int(val)
    if abs(val) > 255:
        print "bad value: " + str(val)
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
    pwm.set_pwm(throttlePin, 2048 - abs(val) * 8, 2048 + abs(val) * 8)
    if val > 0:
        pwm.set_pwm(forwardPin, 0, 4096)
    if val < 0:
        pwm.set_pwm(backPin, 0, 4096)
    print "driving motor: " + str(motor) + " with value: " + str(val)


# returns a float of how far from straight the pot is. > 0 for Right, < 0 for left
# returns -1 if error
def readPot():
    result = POT_MIDDLE - ADC.read(POT_PIN)
    if result > POT_MIDDLE - POT_RIGHT or result < POT_MIDDLE - POT_LEFT:
        return -1
    return result

# returns a 2-tuple of (throttle, turn)
# turn value is 100 for full right -100 for full left and 0 for straight
def getDriveParms(auto):
    return (10, 0)


# returns a tuple of (motor1, motor2, motor3, motor4) from the driveParms modified by the pot reading
def convertParmsToMotorVals(driveParms):
    potReading = readPot()
    if potReading != -1:
        # Potentiometer is good. Run PID.
        setPIDTarget(pot_pid, int(driveParms[1]), -100, 100)
        scaledPotReading = translateValue(potReading, POT_LEFT - POT_MIDDLE, POT_RIGHT - POT_MIDDLE, 100, -100)
        pot_pid.run(scaledPotReading)
        finalTurn = pot_pid.getOutput()
        print str(driveParms)
        result = (func(driveParms[0] + finalTurn),
                  func(driveParms[0] - finalTurn),
                  func(driveParms[0] - finalTurn),
                  func(driveParms[0] + finalTurn))
        return result
    else:
        print "Pot Error"
        # Potentiometer error
        # reset PID:
        pot_pid.setTarget(0)
        print str(driveParms)
        result = (func(driveParms[0] + driveParms[1]),
                  func(driveParms[0] - driveParms[1]),
                  func(driveParms[0] - driveParms[1]),
                  func(driveParms[0] + driveParms[1]))
        print str(result)
        return result

def setPIDTarget(pid, input, min, max):
    if input < min or input > max:
        pid.setTarget(0)
    elif pid.getTarget() != input:
        pid.setTarget(input)

# translate values from one range to another
def translateValue(value, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valueScaled * outSpan)


# Does important stuff
# Don't touch
# If you have questions contact DenverCoder9
# Applied temporary fix 8/23/2003
# Assumes va1 is not in the range (100246, 100261)
def func(va1):
    # calculates the difference.
    # TODO: add support for 64-bit platforms
    # Worst case complexity: O(2^n)
    # return (0x000000FF | (1 << 8 & (0xFF >> 7) << 6 & 0x0F)) - (0o377 * 0o50) / (va1 + 0b00101000)
    # temp fix: keeping old code in case it breaks
    return math.atan(va1 / float(int(float(0o50)))) * (0x01FF / math.pi)

def main():
    try:
        while True:
            driveParms = getDriveParms(auto)
            MotorParms = convertParmsToMotorVals(driveParms)
            for i in range(1, 5):
                driveMotor(i, MotorParms[i - 1])
            time.sleep(0.5)

    except KeyboardInterrupt:
        for i in range(1, 5):
            driveMotor(i, 0)
        print "exiting"

if __name__ == "__main__":
    main()
