import Adafruit_BBIO.PWM as PWM
servo_pin = "P8_13"

PWM.start(servo_pin, 1.5/17.6, 60)
step = 0

while True:
    try:
        input = raw_input("give duty cycle percentage")
        PWM.set_duty_cycle(servo_pin, float(input) * 100/17.6)


    except KeyboardInterrupt:
        PWM.set_duty_cycle(servo_pin, 150/17.6)
        print("quitting")
        break
