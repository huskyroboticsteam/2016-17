#include "WheelController.h"

const int SAMPLE_SIZE = 1000; // in ms

WheelController::WheelController(Adafruit_DCMotor *motor, int *encoder_count) {
  this->motor = motor;
  this->encoder_count = encoder_count;
  this->last_calc_time = millis();
  this->ang_vel = 0.0;
}

// TODO use ang_vel
void WheelController::setSpeed(double speed) {
  motor->setSpeed(min(255, abs(speed)));
  if (speed > 0) {
    motor->run(FORWARD);
  } else {
    motor->run(BACKWARD);
  }
}

void WheelController::calcAngVel() {
  // Motor is 48:1 gearing, with an 8 pole magnet, meaning 1 roation is 384 ticks
  // Checks to see if the sample taking time is up. If yes then it calculates angular velocity
  if (millis() - last_calc_time > SAMPLE_SIZE) {
    // Calculates the angular velocity 
    ang_vel = (double(*encoder_count)/384)/(SAMPLE_SIZE/1000.0);
    // Resets the time for this motor
    last_calc_time = 0;
    // Resets encoder count so we don't double count in the future
    *encoder_count = 0;
  }
}
