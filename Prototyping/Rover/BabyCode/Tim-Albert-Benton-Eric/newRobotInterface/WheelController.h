#ifndef WHEEL_CONTROLLER_H
#define WHEEL_CONTROLLER_H

#include <Adafruit_MotorShield.h>

// An interface for controlling one wheel.
class WheelController {
    public:
        // Constructs a WheelController that controls the wheel with the motor
        // 'motor'.
        WheelController(Adafruit_DCMotor *motor);
        // Makes the wheel turn at 'speed' revolutions per second.
        void setSpeed(double speed);
    private:
        Adafruit_DCMotor *motor;
};
#endif
