#include "Potentiometer.h"

// The pin the potentiometer is connected to.
const int POTENTIOMETER_PIN = 3;
// POTENTIOMETER_VALUE_1 is the value read from the potentiometer when the angle
// is ANGLE_1. Same for POTENTIOMBER_VALUE_2 and ANGLE_2. These angles should be
// extreme left and extreme right, respectively.
const double ANGLE_1 = -45.0;
const double POTENTIOMETER_VALUE_1 = 160;
const double ANGLE_2 = 45.0;
const double POTENTIOMETER_VALUE_2 = 380;

double getCurrentAngle() {
  return map(analogRead(POTENTIOMETER_PIN),
        POTENTIOMETER_VALUE_1, POTENTIOMETER_VALUE_2, ANGLE_1, ANGLE_2);
}
