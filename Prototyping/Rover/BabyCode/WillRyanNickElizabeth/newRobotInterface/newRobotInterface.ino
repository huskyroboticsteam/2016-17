#include "RobotController.h"
#include "Potentiometer.h"
#include "log.h"
#include <SoftwareSerial.h>
int throttle;
int turn;
SoftwareSerial bluetooth(10, 11); // RX, TX

RobotController *controller;
int mode = 1;

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  bluetooth.println("Initialized");
  controller = new RobotController();
}

void loop() {
  int toSend = 63;
  if(bluetooth.available() > 0){
    toSend = bluetooth.read();
  }
  if(toSend < 127){ 
    throttle = (toSend - 63) * -4;
  } else {
    turn = (toSend - 192) * 2/3;
  }
  controller->setDrive(throttle, turn, getCurrentAngle());
}
