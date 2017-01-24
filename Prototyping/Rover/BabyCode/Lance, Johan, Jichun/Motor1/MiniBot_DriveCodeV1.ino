// Current Version could give angular velocity of one motor correctly but not all four.  
// println inside calcAngVel doesn't give any ouput right

#include <Adafruit_MotorShield.h>
Adafruit_DCMotor * motor1;
Adafruit_DCMotor * motor2;
Adafruit_DCMotor * motor3;
Adafruit_DCMotor * motor4;

int SampleSize = 1000; // in ms
int power = 80;
int turn = 0;
long Time = millis();
int PowerMods[4];
int TurnMods[4];
volatile int EncoderCount[4];// = {0,0,0,0};
double AngVel[4];// = {0,0,0,0};

//Pot readings
//Right_turn max value = 820 
//Left_turn max value = 390 
//Straight_ max value = 640

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Adafruit_MotorShield AFMS = Adafruit_MotorShield();
  AFMS.begin();
  motor1 = AFMS.getMotor(1);
  motor2 = AFMS.getMotor(2);
  motor3 = AFMS.getMotor(3);
  motor4 = AFMS.getMotor(4);
  
  motor1->setSpeed(0);
  motor2->setSpeed(0);
  motor3->setSpeed(0);
  motor4->setSpeed(0);

  attachInterrupt(digitalPinToInterrupt(18), count0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), count1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(20), count2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), count3, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:
  Drive(power, turn);
  motor1->run(BACKWARD);
  motor2->run(FORWARD);
  // motor3->run(FORWARD);
  // motor4->run(BACKWARD);
  // for (int i = 0; i < 4; i++) {
    //CalcAngVel(0);
    CalcAngVel(1);
  // }
 // Serial.println( AngVel[0]);
//  Serial.print("\t");
//  Serial.println(AngVel[1]);
//  Serial.print("\t");
//  Serial.print(AngVel[2]);
//  Serial.print("\t");
//  Serial.println(AngVel[3]);
}

void Drive(int power, int turn) {
  PowerMod(power);
  TurnMod(turn);
  motor1->setSpeed(PowerMods[0]+TurnMods[0]);
  motor2->setSpeed(PowerMods[1]+TurnMods[1]);
  motor3->setSpeed(PowerMods[2]+TurnMods[2]);
  motor4->setSpeed(PowerMods[3]+TurnMods[3]);
}

void PowerMod(int power) {
  for (int i = 0; i<=3; i++) {
    PowerMods[i] = power;
  }
} 

// probably going to turn in a PID with the pot
void TurnMod(int turn) { 
  TurnMods[0] = turn;
  TurnMods[1] = -turn;
  TurnMods[2] = -turn;
  TurnMods[3] = turn;
}


void count0() {
    EncoderCount[0]++;
}

void count1() {
    EncoderCount[1]++;
}

void count2() {
    EncoderCount[2]++;
}

void count3() {
    EncoderCount[3]++;
}

void CalcAngVel(int motorNum) {
  
  // Motor is 48:1 gearing, with an 8 pole magnet, meaning 1 roation is 384 ticks
  // Some local variables for the function
  //Checks to see if the sample taking time is up. If yes then it calculates angular velocity
  if (millis() - Time > SampleSize) {
    AngVel[motorNum] = (double(EncoderCount[motorNum])/384)/(SampleSize/1000.0);
    Time = millis();
    Serial.println( AngVel[motorNum]);
  // Resets encoder count so we don't double count in the future
  EncoderCount[motorNum] = 0;
  }
}
