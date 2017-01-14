#include "RobotController.h"

RobotController *controller;

void setup() {
  controller = new RobotController();
  controller->setDrive(100, 30, 0);
}

void loop() {
}
