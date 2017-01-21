#include "RobotController.h"
#include "log.h"

RobotController *controller;

void setup() {
  initLogging();
  controller = new RobotController();
}

void loop() {
  controller->setDrive(10, 20, 20);
}
