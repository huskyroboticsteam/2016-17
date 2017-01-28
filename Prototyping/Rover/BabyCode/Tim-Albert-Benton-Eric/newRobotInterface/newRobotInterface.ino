#include "RobotController.h"
#include "Potentiometer.h"
#include "log.h"

RobotController *controller;
int mode = 1;

void setup() {
  controller = new RobotController();
}

void loop() {
  if (Serial.available() >= 1) {
    int read_mode = Serial.read() - '0';
    if (read_mode != 0) {
      mode = read_mode;
    }
  }
  const int mode_speeds[8] = {0, 0, 30, 30, 30, -30, -30, -30};
  const int mode_angles[8] = {0, 0, 0, -30, 30, 0, -30, 30};
  controller->setDrive(mode_speeds[mode], mode_angles[mode], getCurrentAngle());
}
