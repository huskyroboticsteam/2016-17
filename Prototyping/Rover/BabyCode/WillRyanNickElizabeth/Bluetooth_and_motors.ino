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
  bluetooth.println("Initializing");
}

void loop() {
  char toSend = (char)bluetooth.read();
  Serial.print(toSend);
  if(toSend == 'f') {
    motor1->run(BACKWARD);
    motor2->run(FORWARD);
    motor3->run(BACKWARD);
    motor4->run(FORWARD);
  } else if(toSend == 's') {
    motor1->run(RELEASE);
    motor2->run(RELEASE);
    motor3->run(RELEASE);
    motor4->run(RELEASE);
  }
}

