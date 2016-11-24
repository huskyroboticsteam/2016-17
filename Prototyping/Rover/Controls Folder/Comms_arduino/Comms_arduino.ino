#include "Arduino.h"
#include "config.h"
#include <Servo.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

EthernetUDP Udp;
byte MAC_ADDRESS[] = {0x90, 0xA2, 0xDA, 0x00, 0x3D, 0x8D};
IPAddress IP(192, 168, 1, 40);
// structs for send/ recieve
recieveData recievedPacket;
sendData sentPacket;
bool networkStatus = true;
bool hasIP = false;
unsigned long timeLastPacket; // to be set to millis() in main code
// speed of rover
int throttle = 0;
// turn angle: 0 is straight, < 0 left, > 0 right
int turn = 0;
// who is in control
bool autoPilot = false;

Servo Throttle_Servo;
Servo Turn_Servo;
Servo AutoPilot_Servo;

void setup() {
  Serial.begin(9600);
  initializeWirelessCommunication();
  Serial.println("setup");
  Throttle_Servo.attach(THROTTLE_PIN);
  Turn_Servo.attach(TURN_PIN);
  AutoPilot_Servo.attach(AUTOPILOT_PIN);
  Serial.println("SETUP");
}

void loop() {
  
  receiveWirelessData();
  parseWirelessData();
  sendPWM();
  
}

void sendPWM() {
  /*
  Serial.println("Throttle: " );
  Serial.println(throttle);
  Serial.println("Turn: ");
  Serial.println(turn);
  Serial.println("AutoPilot: ");
  Serial.println(autoPilot);
  Throttle_Servo.writeMicroseconds(map(throttle, 0, 255, THROTTLE_MIN, THROTTLE_MAX));
  Turn_Servo.writeMicroseconds(map(turn, -127, 128, TURN_MIN, TURN_MAX));
  if (autoPilot) {
    AutoPilot_Servo.writeMicroseconds(AUTOPILOT_ON);
  }else {
    AutoPilot_Servo.writeMicroseconds(AUTOPILOT_OFF);

  }
  */
}


