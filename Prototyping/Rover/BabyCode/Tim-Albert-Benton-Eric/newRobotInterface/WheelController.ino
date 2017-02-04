#include "WheelController.h"

WheelController::WheelController(Adafruit_DCMotor *motor) {
  this->motor = motor;
}

void WheelController::setSpeed(double speed) {
  motor->setSpeed(min(255, abs(speed)));
  if (speed > 0) {
    motor->run(FORWARD);
  } else {
    motor->run(BACKWARD);
  }
}
