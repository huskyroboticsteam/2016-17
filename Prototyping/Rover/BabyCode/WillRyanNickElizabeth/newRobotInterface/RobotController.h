#ifndef ROBOT_CONTROLLER_H
#define ROBOT_CONTROLLER_H

#include "PidController.h"
#include <Adafruit_MotorShield.h>

// An interface for controlling the robot.
// All speeds are measured in TODO units. All angles are measured in degrees.
class RobotController {
  public:
    RobotController();
    // Steers the robot. 'target_speed' is the target speed 'target_angle'
    // controlls how the robot should turn. It is the angle we want the
    // central joint to be. 0 is straight forward.  Positive is turning
    // right. Negative is turning left.  'curr_angle' is the current angle
    // of the joint.
    void setDrive(double target_speed, double target_angle, double curr_angle);
  private:
    // Sets 'motor_speeds' such that, if the wheels are maintained at these
    // speeds for a long time, will result in the robot moving at 'speed'
    // and has the central joint at 'angle'.
    void setDriveTowards(double speed, double angle);
    // Adjusts 'motor_speeds' so that the angle is closer to 'target_angle',
    // using the PID controller algorithm.
    void pidAngleCorrection(double target_angle, double curr_angle);
    // Actually make the wheel turn at the values in 'motor_speeds'.
    void setMotors();

    Adafruit_MotorShield motor_shield;
    // PID controller for the angle.
    PidController angle_controller;
    // 0 is back left, 1 is back right, 2 is front left, 3 is front right
    double motor_speeds[4];
    Adafruit_DCMotor *(motors[4]);
};

#endif
