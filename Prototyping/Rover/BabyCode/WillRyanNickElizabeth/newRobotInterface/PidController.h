#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

// Implements a PID controller.
class PidController {
  public:
    // k_p, k_i, and k_d are the constants for the PID controller. They
    // should all be non-negative.
    PidController(double k_p, double k_i, double k_d);
    // This function should be called at regular intervals. 'error' is the
    // error value of the system, which is the current value (process
    // variable) subtracted by the target value (setpoint). Returns how much
    // to correct the error (control variable).
    double go(double error);
  private:
    const double k_p, k_i, k_d;
    // The 'error' value in the previous call to 'go'.
    double prev_error;
    // The sum of 'error' values in all previous calls to 'go'.
    double sum_error;
    // Timestamp of the time 'go' was previously called.
    unsigned long last_called_micros;
    // Is true iff 'go' has been called before.
    bool called_before;
};

#endif
