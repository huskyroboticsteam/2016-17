import time
from Motor import TalonMC

MotorTest = TalonMC("P8_13")

MotorTest.enable()
MotorTest.set(1.0)

for n in range(0, 100):
    MotorTest.set(n / 100.0)
    time.sleep(0.5)

time.sleep(5)
MotorTest.stopAll()
