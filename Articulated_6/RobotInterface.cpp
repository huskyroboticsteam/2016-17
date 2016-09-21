#include "Arduino.h"
#include "RobotInterface.h"

void RobotInterface::initialize() {
  
  for(int i=0; i<4; i++) {
    motors[i].attach(motorPins[i]);
  }
  
  stopMotors();

  FRONT_LENGTH = 7;
  BACK_LENGTH = 9;
  WIDTH = 12;

  L_1 = 7;
  L_2 = 6;
  L_3 = 12;
}

void RobotInterface::setDrive(int throttleIn, int turnIn) {
  throttle = throttleIn;
  turn = turnIn;
  /*
  Serial.print("Setting Drive: ");
  Serial.print(throttle);
  Serial.print(" ");
  Serial.println(turn);
  */
}

void RobotInterface::calculateDrive() {
  float curAngle = map(analogRead(A0), 445, 850, 60, -60);
  curAngle = curAngle * 6.28 / 360;
  articulated_speeds(turn, throttle, curAngle/2);
}

void RobotInterface::pidCalculation() {
  int curAngle = map(analogRead(A0), 445, 850, 60, -60);
  int error = curAngle - turn;
  int output = 2*error;
  motorSpeeds[0] = motorSpeeds[0] - output;
  motorSpeeds[1] = motorSpeeds[1] + output;
  motorSpeeds[2] = motorSpeeds[2] + output;
  motorSpeeds[3] = motorSpeeds[3] - output;
  
  int maxSpeed = 0;
  for (int i=0; i<sizeof(motorSpeeds); i++) {
    if (abs(motorSpeeds[i]) > maxSpeed)
      maxSpeed = abs(motorSpeeds[i]);
  }
  if (maxSpeed > 100) {
    for (int i=0; i<sizeof(motorSpeeds); i++) {
      motorSpeeds[i] = map(motorSpeeds[i], -maxSpeed, maxSpeed, -100, 100);
    }
  }
}

// Accepts values -100 to 100, and sets motor speeds accordingly
void RobotInterface::writeToMotors() {
  motors[0].writeMicroseconds(map(motorSpeeds[0], -100, 100, MOTOR_OUT_MIN, MOTOR_OUT_MAX));
  motors[1].writeMicroseconds(map(motorSpeeds[1], -100, 100, MOTOR_OUT_MAX, MOTOR_OUT_MIN));
  motors[2].writeMicroseconds(map(motorSpeeds[2], -100, 100, MOTOR_OUT_MIN, MOTOR_OUT_MAX));
  motors[3].writeMicroseconds(map(motorSpeeds[3], -100, 100, MOTOR_OUT_MAX, MOTOR_OUT_MIN));
}

void RobotInterface::printMotorSpeeds() {
  Serial.print("Motor Speeds: ");
  for (int i=0; i<4; i++) {
    Serial.print(motorSpeeds[i]); Serial.print(" ");
  }
  Serial.println();
}

// Stops the motors.
// To calibrate continuous servos, call stopMotors(), then adjust
// the screws until motion stops.
void RobotInterface::stopMotors() {
  Serial.println("Stopping the motors!");
  for(int i=0; i<sizeof(motors); i++) {
    motors[i].writeMicroseconds(1450);
  }
}

void RobotInterface::testMotorPins() {
  for (int i=0; i<4; i++) {
    for(int j=0; j<4; j++) {
      motorSpeeds[j] = 0;
    }
    motorSpeeds[i] = 100;
    printMotorSpeeds();
    writeToMotors();
    delay(3000);
  }
}


float RobotInterface::articulated_speeds(float joystick_x, float joystick_y, float theta) {
  float radius = 0;
  //just so it doesn't have to calculate infinite radiuses. I'm not actually going to write go_straight cause its boring.
  if (abs(theta) <= .5/57.3)  {
    radius = go_straight(joystick_y);
  } else {
    radius = forward_speed(joystick_y, theta);
  }

  //Changes the wheel speeds individualy to allow for turning in.
  //there is almost certianly a better way, but this was easy and functional.
  float turning_constant = .75;
  float d_speed = turning_constant * joystick_x;
  motorSpeeds[0] = motorSpeeds[0] - d_speed;
  motorSpeeds[1] = motorSpeeds[1] + d_speed;
  motorSpeeds[2] = motorSpeeds[2] + d_speed;
  motorSpeeds[3] = motorSpeeds[3] - d_speed;

  //there is honestly plenty of other stuff i could put in, i just don't feel like it. i will list it out though:
  //
  //  speed change caps
  //      basically limit how much any individual wheel speed can change per whatever. to do it, take the difference between your current target speeds
  //      and your past speeds and pull out the max absolute change. if that guy is over your speed change max, scale down all the CHANGES and then add them back
  //      to your PREVIOUS values.
  //
  //  speed caps
  //      pretty much same thing as speed change caps but with the actual speed values IE no trying to go over %100 on any of the wheels. scale all down appropriately.
  //
  //  theta caps
  //      stops it from turning any more if it hits a certian angle.
  return radius;
}

float RobotInterface::forward_speed(float joystick_y, float theta) {
  //finds the two lengths
  float L_4 = L_1 * cos(2 * theta);
  float L_5 = L_1 * sin(2 * theta);

  //using math i calculated out on paper, this is the radius
  float radius = ((L_3 * L_4) / L_5) + ((L_4 * L_4) / L_5) + L_5;

  float radius_right = radius - L_2;
  float radius_left = radius + L_2;
  float base_speed = joystick_y * speed_constant;
  float right_speed = base_speed * radius_right / radius;
  float left_speed = base_speed * radius_left / radius;

  motorSpeeds[0] = right_speed;
  motorSpeeds[1] = left_speed;
  motorSpeeds[2] = right_speed;
  motorSpeeds[3] = left_speed;
  
  return radius;
}

float RobotInterface::go_straight(float joystick_y) {
  motorSpeeds[0] = joystick_y * speed_constant;
  motorSpeeds[1] = joystick_y * speed_constant;
  motorSpeeds[2] = joystick_y * speed_constant;
  motorSpeeds[3] = joystick_y * speed_constant;
  float radius = 0;
  return radius;
}


