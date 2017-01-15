#include "PidController.h"

PidController::PidController(double k_p, double k_i, double k_d):
  k_p(k_p), k_i(k_i), k_d(k_d), prev_error(0.0), sum_error(0.0) {}

double PidController::go(double error) {
  double diff_error = error - prev_error;
  sum_error += error;
  prev_error = error;
  return error * k_p + sum_error * k_i + diff_error * k_d;
}
