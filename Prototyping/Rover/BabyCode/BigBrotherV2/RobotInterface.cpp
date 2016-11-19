#include "Arduino.h"
#include "RobotInterface.h"

void RobotInterface::initialize() {
  for (int i=0; i<4; i++) {
    motors[i] = new AF_DCMotor(i+1, MOTOR12_64KHZ);
  }
  curMode = ACTIVE;
  //stopMotors();
}

// Sets the variables in this class.  Motor speeds calculated elsewhere
void RobotInterface::setDrive(int throttleIn, int turnIn) {
  throttle = throttleIn;
  turn = turnIn;
}

void RobotInterface::readSensors() {
  curAngle = map(analogRead(A0), 279, 539, 30, -30);
  timeLastRead = millis(); // Critical for PID calculation
}

void RobotInterface::passiveHingeDrive() {
  Serial.println(curAngle);
  float wheelRatio[4] = {0, 0, 0, 0};
  if (curAngle == 0) { // math breaks if calculated with angle = 0
    for (int i=0; i<4; i++) {
      wheelRatio[i] = throttle;
    }
  } else {
    float angleRads = (float) curAngle * 6.28 / 360.0;
    float constant = FRONT_LENGTH + BACK_LENGTH/cos(angleRads);
    float frontRadius = constant / tan(angleRads);
    float backRadius = constant / sin(angleRads) - BACK_LENGTH * tan(angleRads);
    // Front Left, Front Right, back left, back Right
    float wheelRatio[] = {
      frontRadius + WIDTH/2, 
      frontRadius - WIDTH/2, 
      backRadius + WIDTH/2, 
      backRadius - WIDTH/2
    };

    // make fastest motor speed porportional to throttle, and adjust others accordingly
    float maxDistance = 0;
    for (int i=0; i<4; i++) {
      if (abs(wheelRatio[i]) > abs(maxDistance)) {
        maxDistance = wheelRatio[i];
      }
    }
    for (int i=0; i<4; i++) {
      motorSpeeds[i] = map(wheelRatio[i], -maxDistance, maxDistance, -throttle, throttle);
    }
    
    float turnConstant = 2;
    motorSpeeds[0] = motorSpeeds[0] + turnConstant * turn;
    motorSpeeds[1] = motorSpeeds[1] - turnConstant * turn;
  }
}

void RobotInterface::activeHingeDrive() {
  if (curAngle == 0) {
    for (int i=0; i<4; i++) {
      motorSpeeds[i] = throttle;
    }
    pidCalculation();
    return;
  }
  
  float turnRads = (float) turn * 6.28 / 360.0;
  float constant = FRONT_LENGTH + BACK_LENGTH/cos(turnRads);
  float frontRadius = constant / tan(turnRads);
  float backRadius = constant / sin(turnRads) - BACK_LENGTH * tan(turnRads);
  // Front Left, Front Right, back left, back Right
  float wheelRatio[] = {
    frontRadius + WIDTH/2, 
    frontRadius - WIDTH/2, 
    backRadius + WIDTH/2, 
    backRadius - WIDTH/2
  };
  float maxDistance = 0;
  for (int i=0; i<4; i++) {
    if (abs(wheelRatio[i]) > abs(maxDistance)) {
      maxDistance = wheelRatio[i];
    }
  }
  for (int i=0; i<4; i++) {
    motorSpeeds[i] = map(wheelRatio[i], -maxDistance, maxDistance, -throttle, throttle);
  }
  pidCalculation();
}

void RobotInterface::drive() {
  if(curMode == ACTIVE) {
    activeHingeDrive();
  }
  if (curMode == PASSIVE) {
    passiveHingeDrive();
  }
}

void RobotInterface::pidCalculation() {
  //Serial.println("BeginPID");
  //printMotorSpeeds();
  float error = curAngle - turn;
  errorI += error;
  if(kI*errorI > maxI) {
    errorI = maxI / kI;
  }
  float dError = lastError - error;
  lastError = error;
  float output = kP*error + kI*errorI + kD * dError;

//  Uncomment for Debugging information
//  Serial.print(kP*error);  Serial.print(" ");
//  Serial.print(kI*errorI);  Serial.print(" ");
//  Serial.print(kD*dError); Serial.print(" ");
//  Serial.println(lastError);

  motorSpeeds[0] -= output;
  motorSpeeds[1] += output;
  
  int maxSpeed = 0;
  for (int i=0; i<sizeof(motorSpeeds); i++) {
    if (abs(motorSpeeds[i]) > maxSpeed)
      maxSpeed = abs(motorSpeeds[i]);
  }
  if (maxSpeed > 100) {
    for (int i=0; i<4; i++) {
      motorSpeeds[i] = map(motorSpeeds[i], -maxSpeed, maxSpeed, -100, 100);
    }
  }
  //printMotorSpeeds();
  //Serial.println("EndPID");
}

// Accepts values -100 to 100, and sets motor speeds accordingly
void RobotInterface::writeToMotors() {
  int outputValues[4];
  int outputDirections[] = {1, 1, 1, 1};
  for (int i=0; i<4; i++) {
    int theSpeed = motorSpeeds[i];
    if (theSpeed < 0) {
      outputDirections[i] = -1;
      theSpeed = -theSpeed;
    }
    motors[i]->setSpeed(map(theSpeed, 0, 100, 0, 255));
  }
  for (int i=0; i<4; i++) {
    if (outputDirections[i] == 1) {
      motors[i]->run(FORWARD);
    }
    else {
      motors[i]->run(BACKWARD);
    }
  }
}

void RobotInterface::printMotorSpeeds() {
  Serial.print("Motor Speeds: ");
  for (int i=0; i<4; i++) {
    Serial.print(motorSpeeds[i]); Serial.print(" ");
  }
  Serial.println();
}

void RobotInterface::printDrive() {
  Serial.print("Throttle: "); Serial.print(throttle);
  Serial.print(" Turn: "); Serial.println(turn);
}

// Stops the motors.
void RobotInterface::stopMotors() {
  for (int i=0; i<4; i++) {
    motors[i]->run(RELEASE);
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



