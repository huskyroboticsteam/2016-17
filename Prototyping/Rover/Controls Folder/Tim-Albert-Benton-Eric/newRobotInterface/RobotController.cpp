#include "RobotController.h"
#include <math.h>

// The distance between the left and right wheels.
const double WIDTH = 1.0;  // TODO measure this
// The distance between the front and back wheels.
const double LENGTH = 1.0; // TODO measure this
// Constants for the PID controller.
const double K_P = 0.0, K_I = 0.00, K_D = 0.00000; // TODO tune these
// Epsilon: numbers less than this is treated as zero.
const double EPS = 1e-4;

RobotController::RobotController(): angle_controller(K_P, K_I, K_D) {
    motor_shield.begin();
    for (int i = 0; i < 4; i++) {
        motors[i] = motor_shield.getMotor(i+1);
    }
}

void RobotController::setDrive(
        double target_speed, double target_angle, double curr_angle) {
    double error = curr_angle - target_angle;
    double correction = angle_controller.go(error);
    setDriveTowards(target_speed, curr_angle + correction);
    setMotors();
}

void RobotController::setDriveTowards(double speed, double angle) {
    if (angle < EPS) { // If going straight forward.
        for (int i = 0; i < 4; i++) {
            motor_speeds[i] = speed;
        }
        return;
    }
    // Convert to radians
    double angle_rad = angle * M_PI / 180.0;
    // Turning radius. Positive if turning right. Negative if turning left.
    double r = LENGTH / (2 * tan(angle_rad / 2));
    double left_speed =  speed * (r + WIDTH / 2) / r;
    double right_speed = speed * (r - WIDTH / 2) / r;
    motor_speeds[0] = left_speed;
    motor_speeds[1] = right_speed;
    motor_speeds[2] = right_speed;
    motor_speeds[3] = left_speed;
}

void RobotController::setMotors() {
    // The left wheels have to turn the other way
    const double MULTIPLIER[4] = {-1, 1, 1, -1};
    for (int i = 0; i < 4; i++) {
        double x = motor_speeds[i] * MULTIPLIER[i];
        if (x > 0) {
            motors[i]->setSpeed(x);
            motors[i]->run(FORWARD);
        } else {
            motors[i]->setSpeed(x);
            motors[i]->run(BACKWARD);
        }
    }
}
