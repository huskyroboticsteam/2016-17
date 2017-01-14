#include "RobotController.h"
#include <math.h>

// The distance between the left and right wheels.
const double WIDTH = 1.0;  // TODO measure this
// The distance between the front and back wheels.
const double LENGTH = 1.0; // TODO measure this
// Constants for the PID controller.
const double K_P = 1.5, K_I = 0.01, K_D = 0.00001; // TODO tune these
// Epsilon: numbers less than this is treated as zero.
const double EPS = 1e-4;

RobotController::RobotController(): angle_controller(K_P, K_I, K_D) {
    // TODO set up motors
}

void RobotController::setDrive(
        double target_speed, double target_angle, double curr_angle) {
    double error = curr_angle - target_angle;
    double correction = angle_controller.go(error);
    setDriveTowards(target_speed, curr_angle + correction);
}

void RobotController::setDriveTowards(double speed, double angle) {
    if (angle < EPS) { // If going straight forward.
        setMotor(speed, speed);
        return;
    }
    // Convert to radians
    double angle_rad = angle * M_PI / 180.0;
    // Turning radius. Positive if turning right. Negative if turning left.
    double r = LENGTH / (2 * tan(angle_rad / 2));
    double left_speed =  speed * (r + WIDTH / 2) / r;
    double right_speed = speed * (r - WIDTH / 2) / r;
    setMotor(left_speed, right_speed);
}

void RobotController::setMotor(double left_speed, double right_speed) {
    // TODO
}
