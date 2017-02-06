#include "RobotController.h"
#include "Potentiometer.h"
#include "log.h"
#include <SoftwareSerial.h>
int throttle;
int turn;
SoftwareSerial bluetooth(10, 11); // RX, TX
boolean initialized;
boolean leftInitialized;
boolean rightInitialized;
int left;
int right;
const int POTENTIOMETER_PIN = 3;

RobotController *controller;
int mode = 1;

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  bluetooth.println("Initialized");
  controller = new RobotController();
  initialized = false;
  leftInitialized = false;
  rightInitialized = false;
}

void loop() {
  int toSend = 63;
  if(bluetooth.available() > 0){
    toSend = bluetooth.read();
  }
  if(toSend < 127 && toSend > 0){ 
    throttle = (toSend - 63) * -4;
  } else if(toSend > 127) {
    turn = (toSend - 192) * 2/3;
  } else if(toSend == 0) {
    if(!leftInitialized) {
      left = analogRead(POTENTIOMETER_PIN);
      Serial.println("left initiallized");
      leftInitialized = true;
    } else if(!rightInitialized) {
      right = analogRead(POTENTIOMETER_PIN);
      Serial.println("right initialized");
      rightInitialized = true;
    } else {
      calibrate(left, analogRead(POTENTIOMETER_PIN), right);
      Serial.println("middle initialized");
      initialized = true;
    }
  }
  if(initialized) {
    controller->setDrive(throttle, turn, getCurrentAngle());
  }
}
