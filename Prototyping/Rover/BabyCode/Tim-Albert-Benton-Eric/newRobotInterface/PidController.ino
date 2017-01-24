#include "PidController.h"
#include <Arduino.h>

PidController::PidController(double k_p, double k_i, double k_d):
    k_p(k_p), k_i(k_i), k_d(k_d) {
  sum_error = 0.0;
  called_before = false;
}

double PidController::go(double error) {
  double correction = - k_p * error;
  unsigned long curr_micros = micros();
  if (called_before) {
    unsigned long diff_micros = curr_micros - last_called_micros;
    sum_error += error * diff_micros;
    correction -= k_i * sum_error;
    correction -= k_d * (error - prev_error) / max(diff_micros, 1ul);
  }
  prev_error = error;
  last_called_micros = curr_micros;
  called_before = true;
  return correction;
}
