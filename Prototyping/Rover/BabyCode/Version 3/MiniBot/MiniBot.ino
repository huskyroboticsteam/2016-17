#include <Adafruit_MotorShield.h>
Adafruit_DCMotor * motor1, motor2, motor3, motor4;
void setup() {
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
}
void loop() {// put your main code here, to run repeatedly:
  motor1->run(FORWARD);
}
