#include <Adafruit_MotorShield.h>

#include <SoftwareSerial.h>
Adafruit_DCMotor * motor1;
Adafruit_DCMotor * motor2;
Adafruit_DCMotor * motor3;
Adafruit_DCMotor * motor4;
SoftwareSerial bluetooth(10, 11); // RX, TX

void setup() {
  Serial.begin(9600);
  Adafruit_MotorShield AFMS = Adafruit_MotorShield();
  AFMS.begin();
  motor1 = AFMS.getMotor(1);
  motor2 = AFMS.getMotor(2);
  motor3 = AFMS.getMotor(3);
  motor4 = AFMS.getMotor(4);
  motor1->setSpeed(100);
  motor2->setSpeed(100);
  motor3->setSpeed(100);
  motor4->setSpeed(100);
  bluetooth.begin(9600);
  bluetooth.println("Initialized");
}

void loop() {
  // Bluetooth sends character read from serial monitor to arduino which sends to motors
  char toSend = (char)bluetooth.read();
  Serial.println(toSend);
  if(toSend == 'f') { // forward
    motor1->run(BACKWARD);
    motor2->run(FORWARD);
    motor3->run(BACKWARD);
    motor4->run(FORWARD);
  } else if(toSend == 's') { // stop
    motor1->run(RELEASE);
    motor2->run(RELEASE);
    motor3->run(RELEASE);
    motor4->run(RELEASE);
  } else if(toSend == 'r') { // reverse
    motor1->run(FORWARD);
    motor2->run(BACKWARD);
    motor3->run(FORWARD);
    motor4->run(BACKWARD);
  } else if(toSend == 'b') { // boost
    motor1->setSpeed(255);
    motor2->setSpeed(255);
    motor3->setSpeed(255);
    motor4->setSpeed(255);
  } else if(toSend == 'n') { // no boost
    motor1->setSpeed(100);
    motor2->setSpeed(100);
    motor3->setSpeed(100);
    motor4->setSpeed(100);
  }
}
