#include <Adafruit_MotorShield.h>
Adafruit_DCMotor * motor1;
Adafruit_DCMotor * motor2;
Adafruit_DCMotor * motor3;
Adafruit_DCMotor * motor4;
int power; 
int turn; 
int motor1_speed = 0;
int motor2_speed = 0;
int motor3_speed = 0;
int motor4_speed = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Adafruit_MotorShield AFMS = Adafruit_MotorShield();
  AFMS.begin();
  motor1 = AFMS.getMotor(1);
  motor2 = AFMS.getMotor(2);
  motor3 = AFMS.getMotor(3);
  motor4 = AFMS.getMotor(4);
  /*
  motor1->setSpeed(100);
  motor2->setSpeed(100);
  motor3->setSpeed(100);
  motor4->setSpeed(100);*/

  

}

void loop() {
  // put your main code here, to run repeatedly:
  Drive(100, 0);
  motor1->run(BACKWARD);
  motor2->run(BACKWARD);
  motor3->run(BACKWARD);
  motor4->run(BACKWARD);
  delay(1000);
}

void Drive(int power, int turn) {
  motor1_speed = PowerMod(power) + TurnMod(turn); 
  motor2_speed = PowerMod(power) + TurnMod(turn); 
  motor3_speed = PowerMod(power) + TurnMod(turn); 
  motor4_speed = PowerMod(power) + TurnMod(turn); 

  motor1->setSpeed(motor1_speed);
  motor2->setSpeed(motor2_speed);
  motor3->setSpeed(motor3_speed);
  motor4->setSpeed(motor4_speed);
  Serial.print(motor1_speed);
  Serial.print(motor2_speed);
  Serial.print(motor3_speed);
  Serial.println(motor4_speed);
     
}

int PowerMod(int power) { 

 // if (power >= 0)
  int new_power = power;
  return new_power; 
} 

int TurnMod(int turn) { 

  int new_turn = turn; 
  return new_turn; 
}
