#include "Potentiometer.h"
#include "log.h"

// The pin the potentiometer is connected to.
// Number of potentiometer calibration points. Must be at least 2.
const int NUM_CALIBRATION = 3;
// For any i, POTENTIOMETER_VALUES[i] should be the value read from the
// potentiometer when the angle is ANGLES[i]. ANGLES[0] and ANGLES[NUM_CALIBRATION-1]
// should be the extreme left and extreme right in some order. POTENTIOMETER_VALUES
// should be strictly increasing.
const double ANGLES[NUM_CALIBRATION] = {-45.0, 0.0, 45.0};
double POTENTIOMETER_VALUES[NUM_CALIBRATION];

void calibrate(int left, int middle, int right) {
  POTENTIOMETER_VALUES[0] = left;
  POTENTIOMETER_VALUES[1] = middle;
  POTENTIOMETER_VALUES[2] = right;
}

double getCurrentAngle() {
  debugln("Calling getCurrentAngle: ");
  double value = analogRead(POTENTIOMETER_PIN);
  double angle;
  if (value <= POTENTIOMETER_VALUES[0]) {
    debugln("value <= POTENTIOMETER_VALUES[0]");
    angle = ANGLES[0];
  } else if (value >= POTENTIOMETER_VALUES[NUM_CALIBRATION-1]) {
    debugln("value >= POTENTIOMETER_VALUES[NUM_CALIBRATION-1]");
    angle = ANGLES[NUM_CALIBRATION-1];
  } else {
    for (int i = 0; i < NUM_CALIBRATION-1; i++) {
      if (value >= POTENTIOMETER_VALUES[i] && value <= POTENTIOMETER_VALUES[i+1]) {
        debug("In range #"); debugln(i);
        angle = map(value, POTENTIOMETER_VALUES[i], POTENTIOMETER_VALUES[i+1],
              ANGLES[i], ANGLES[i+1]);
        break;
      }
    }
  }
  debuglnValue(value);
  debuglnValue(angle);
  return angle;
}
