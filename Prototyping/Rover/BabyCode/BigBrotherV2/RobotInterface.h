#ifndef RobotInterface_h
#define RobotInterface_h

#include "Arduino.h"
#include "AFMotor.h"

class RobotInterface {
  public:
    void initialize();
    void calculateDrive();
    void setDrive(int throttle, int turn);
    void stopMotors();
    void testMotorPins();
    void writeToMotors();
    void printMotorSpeeds();
    void printDrive();
    void setDriveMode();
    void drive();
    void readSensors();
    enum driveMode {ACTIVE, PASSIVE, SKID};
  private:
    void pidCalculation();
    int throttle;
    int turn;
    int curAngle;
    void passiveHingeDrive();
    void activeHingeDrive();
    driveMode curMode;

    float kP = 3;
    float kI = .02;
    float kD = 0;
    float maxI = 25;
    float errorI = .75;
    float lastError;
    long timeLastRead;

    AF_DCMotor *motors[4];
    int motorSpeeds[4] = {0, 0, 0, 0};

    int FRONT_LENGTH = 0;
    int BACK_LENGTH = 20;
    int WIDTH = 16;

    int MOTOR_OUT_MAX = 0;
    int MOTOR_OUT_MIN = 255;
};
#endif
