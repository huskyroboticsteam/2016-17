#include "RobotController.h"
#include "Potentiometer.h"
#include "log.h"

RobotController *controller;

void setup() {
  initLogging();
  controller = new RobotController();
}

void loop() {
  controller->setDrive(50, -20, getCurrentAngle());
}
