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
  Serial.println("Initialized serial");
  controller = new RobotController();
  initialized = false;
  leftInitialized = false;
  rightInitialized = false;
}

void loop() {
  int toSend = 63;
  if(bluetooth.available() >= 0){
    toSend = bluetooth.read();
  }
  if(toSend < 127 && toSend > 0){ 
    throttle = (toSend - 63) * -4;
  } else if(toSend > 127) {
    turn = (toSend - 192) * 2/3;
  }
  controller->setDrive(throttle, turn, getCurrentAngle());
}
