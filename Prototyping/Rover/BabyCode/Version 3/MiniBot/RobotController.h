#ifndef ROBOT_CONTROLLER_H
#define ROBOT_CONTROLLER_H

#include "PidController.h"

 
// An interface for controlling the robot. Assumes that the joint is exactly in
// the middle between the front and back wheels.
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
        // Sets the wheel speeds such that, if maintained at these speeds for a
        // long time, will result in the robot moving at 'speed' and has the
        // central joint at 'angle'.
        void setDriveTowards(double speed, double angle);
        // Sets the wheel speeds to 'left_speed' and 'right_speed'.
        void setMotor(double left_speed, double right_speed);

       

        
        // PID controller for the angle.
        PidController angle_controller;
};

#endif
