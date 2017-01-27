#include "Potentiometer.h"

// The pin the potentiometer is connected to.
const int POTENTIOMETER_PIN = 3;
// Number of potentiometer calibration points. Must be at least 2.
const int NUM_CALIBRATION = 2;
// For any i, POTENTIOMETER_VALUES[i] should be the value read from the
// potentiometer when the angle is ANGLES[i]. ANGLES[0] and ANGLES[NUM_CALIBRATION-1]
// should be the extreme left and extreme right in some order. POTENTIOMETER_VALUES
// should be strictly increasing.
const double ANGLES[NUM_CALIBRATION] = {-45.0, 45.0};
const double POTENTIOMETER_VALUES[NUM_CALIBRATION] = {160, 380};

double getCurrentAngle() {
  double value = analogRead(POTENTIOMETER_PIN);
  if (value <= POTENTIOMETER_VALUES[0]) {
    return ANGLES[0];
  } else if (value >= POTENTIOMETER_VALUES[NUM_CALIBRATION-1]) {
    return ANGLES[NUM_CALIBRATION-1];
  } else {
    for (int i = 0; i < NUM_CALIBRATION-1; i++) {
      if (value >= ANGLES[i] && value <= ANGLES[i+1]) {
        return map(value, POTENTIOMETER_VALUES[i], POTENTIOMETER_VALUES[i+1],
              ANGLES[i], ANGLES[i+1]);
      }
    }
  }
}
