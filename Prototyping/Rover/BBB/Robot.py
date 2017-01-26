import Adafruit_BBIO.ADC as ADC

ADC.setup()
#Potentiometer pin:
POT_PIN = "AIN0"
POT_LEFT = 0.768
POT_MIDDLE = 0.556
POT_RIGHT = 0.331
POT_TOL = 0.001
#0 if manual 1 if auto drive
auto = 0

#drives the motor with a value, negative numbers for reverse
def driveMotor(motor, val ):
    print "driving motor: " + str(motor)  + " with value: " + str(val)

def readPot():
    return ADC.read(POT_PIN)

#returns a tuple of (throtle, turn)
def getDriveParms(auto):
    return (100, 0)

#returns a tuple of (motor1, motor2, motor3, motor4) from the driveParms modified by the pot reading
def convertParmsToMotorVals(driveParms):
    result = (driveParms[0], driveParms[0], driveParms[0], driveParms[0])
    potReading = readPot()
    return result

def main():
    while True:
        driveParms = getDriveParms(auto)
        MotorParms = convertParmsToMotorVals(driveParms)
        for i in range(4):
            driveMotor(i, MotorParms[i])

if __name__ == "__main__": main()