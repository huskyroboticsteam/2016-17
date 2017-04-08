import Adafruit_BBIO.PWM as PWM
import sys
servo_pin_1 = "P9_14"
servo_pin_2 = "P9_22"
servo_pin_3 = "P8_13"
servo_pin_4 = "P9_28"


PWM.start(servo_pin_1, 1.5/17.6, 60)
PWM.start(servo_pin_2, 1.5/17.6, 60)
PWM.start(servo_pin_3, 1.5/17.6, 60)
PWM.start(servo_pin_4, 1.5/17.6, 60)
step = 0

while True:
    try:
        input = raw_input("give duty cycle percentage")
        PWM.set_duty_cycle(servo_pin_1, float(input) * 100/17.6)
        PWM.set_duty_cycle(servo_pin_2, float(input) * 100/17.6)
        PWM.set_duty_cycle(servo_pin_3, float(input) * 100/17.6)
        PWM.set_duty_cycle(servo_pin_4, float(input) * 100/17.6)


    except KeyboardInterrupt:
        PWM.set_duty_cycle(servo_pin_1, 150/17.6)
        PWM.set_duty_cycle(servo_pin_2, 150/17.6)
        PWM.set_duty_cycle(servo_pin_3, 150/17.6)
        PWM.set_duty_cycle(servo_pin_4, 150/17.6)
        print("quitting")
        break
