#include "SerialPacketManager.h"
#include "SoftwareSerial.h"
#include "RobotInterface.h"

SerialPacketManager xbee(9600);
RobotInterface robot;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Initializing");
  robot.initialize();
  //robot.testMotorPins();
  xbee.onPacketReady = processMessage;
}

void loop() {
  // put your main code here, to run repeatedly:
  xbee.readSerial(50);
  robot.readSensors();
  robot.drive();
  //robot.printMotorSpeeds();
  //robot.printDrive();
  robot.writeToMotors();
}

void processMessage(byte msg[], int msgLength) {
  if (msgLength < 1)
    return;
  if (msg[0] == 20 && msgLength >= 3) {
    int throttle = map(msg[1], 0, 255, -100, 100);
    if (abs(throttle) < 2)
      throttle = 0;
    int turn = map(msg[2], 0, 255, -45, 45);
    if (turn > 30) {
      turn = 30;
    }
    if (turn < -30) {
      turn = -30;
    }
    if (abs(turn) < 1) {
      turn = 0;
    }
    robot.setDrive(throttle, turn);
  }
}

