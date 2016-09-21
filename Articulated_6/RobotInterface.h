#ifndef RobotInterface_h
#define RobotInterface_h

#include "Arduino.h"
#include "Servo.h"

class RobotInterface {
  public:
    void initialize();
    void calculateDrive();
    void setDrive(int throttle, int turn);
    void stopMotors();
    void testMotorPins();
    void writeToMotors();
    void printMotorSpeeds();

    float articulated_speeds(float joystick_x, float joystick_y, float theta);
    float forward_speed(float joystick_y, float theta);
    float go_straight(float joystick_y);
  private:
    void pidCalculation();
    int throttle;
    int turn;
    
    int motorPins[4] = {10, 11, 6, 9};
    Servo motors[4];
    int motorSpeeds[4] = {0, 0, 0, 0};

    Servo motorFL;
    Servo motorFR;
    Servo motorBL;
    Servo motorBR;

    int FRONT_LENGTH = 7;
    int BACK_LENGTH = 7;
    int WIDTH = 12;

    float L_1;
    float L_2;
    float L_3;

    float speed_constant = 1;

    int MOTOR_OUT_MAX = 1600;
    int MOTOR_OUT_MIN = 1300;
};
#endif
