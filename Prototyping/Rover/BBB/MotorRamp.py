# This code ramps up the motor to the desired speed. This is to prevent any damage that occurs
# from sudden acceleration.

def RampMotor():

    rampRate = 10  # chose rate at which to ramp motors at
    change = joystickInput - output  # joystickInput is desired speed, output is the current motor speed

    if change > rampRate:
        change = rampRate

    elif change < -rampRate:
        change = -rampRate

    output += change
    return output
