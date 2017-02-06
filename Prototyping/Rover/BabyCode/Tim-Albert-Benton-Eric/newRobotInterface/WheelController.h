#ifndef WHEEL_CONTROLLER_H
#define WHEEL_CONTROLLER_H

#include <Adafruit_MotorShield.h>

// An interface for controlling one wheel.
class WheelController {
    public:
        WheelController(Adafruit_DCMotor *motor, volatile int *encoder_count);
        // Makes the wheel turn at 'speed' revolutions per second.
        void setSpeed(double speed);
    private:
        // Sets ang_vel to current angular velocity
        void calcAngVel();

        Adafruit_DCMotor *motor;
        volatile int *encoder_count;
        long unsigned int last_calc_time;
        // Current angular velocity
        double ang_vel;
};
#endif
