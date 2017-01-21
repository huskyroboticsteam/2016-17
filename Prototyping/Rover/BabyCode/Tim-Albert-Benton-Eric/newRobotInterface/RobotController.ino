#include "RobotController.h"
#include "Potentiometer.h"
#include <math.h>

// All lengths are measured in TODO units
// The distance between the left and right wheels.
const double WIDTH = 1.0;  // TODO measure this
// The distance between the front wheels and the middle joint.
const double FRONT_LENGTH = 0.5; // TODO measure this
// The distance between the back wheels and the middle joint.
const double BACK_LENGTH = 0.5; // TODO measure this
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
  setDriveTowards(target_speed, curr_angle);
  pidAngleCorrection(target_angle, curr_angle);
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
  // Have different values for front and back wheels.
  double r_front = (BACK_LENGTH + FRONT_LENGTH * cos(angle_rad)) / sin(angle_rad);
  double r_back  = (FRONT_LENGTH + BACK_LENGTH * cos(angle_rad)) / sin(angle_rad);
  motor_speeds[0] = speed * (1 + WIDTH / (2 * r_back)); // back left wheel
  motor_speeds[1] = speed * (1 - WIDTH / (2 * r_back)); // back right wheel
  motor_speeds[2] = speed * (1 + WIDTH / (2 * r_front)); // front left wheel
  motor_speeds[3] = speed * (1 - WIDTH / (2 * r_front)); // front right wheel
}

void RobotController::pidAngleCorrection(
    double target_angle, double curr_angle) {
  double error = curr_angle - target_angle;
  double correction = angle_controller.go(error);
  motor_speeds[0] -= correction;
  motor_speeds[1] += correction;
  motor_speeds[2] += correction;
  motor_speeds[3] -= correction;
}

void RobotController::setMotors() {
  // The left wheels have to turn the other way
  const double MULTIPLIER[4] = {-1, 1, -1, 1};
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
