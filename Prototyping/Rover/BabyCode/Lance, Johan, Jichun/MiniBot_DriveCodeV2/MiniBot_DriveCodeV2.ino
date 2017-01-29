#include <Adafruit_MotorShield.h>
Adafruit_DCMotor * motor1;
Adafruit_DCMotor * motor2;
Adafruit_DCMotor * motor3;
Adafruit_DCMotor * motor4;

int SampleSize = 1000; // in ms
long unsigned int Time[] = {millis(),millis(),millis(),millis()};
int PowerMods[4];
int TurnMods[4];
volatile int EncoderCount[4];// = {0,0,0,0};
double AngVel[4];// = {0,0,0,0};

//Pot readings
//Right_turn max value = 820 
//Left_turn max value = 390 
//Straight_ max value = 640

void setup() {
  Serial.begin(9600);

  // Set up needed for motors
  Adafruit_MotorShield AFMS = Adafruit_MotorShield();
  AFMS.begin();
  motor1 = AFMS.getMotor(1);
  motor2 = AFMS.getMotor(2);
  motor3 = AFMS.getMotor(3);
  motor4 = AFMS.getMotor(4);

  // init all motors to 0
  motor1->setSpeed(0);
  motor2->setSpeed(0);
  motor3->setSpeed(0);
  motor4->setSpeed(0);

  // interrupts used to count encoder ticks
  attachInterrupt(digitalPinToInterrupt(2), count0, CHANGE);
  attachInterrupt(digitalPinToInterrupt(3), count1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(18), count2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), count3, CHANGE);
}

void loop() {
  // input power and turn. Right now is constant, but can be replaced by comm input.
  int power = 0;
  int turn = 0;
  
  // calls the drive function that sets motor speeds
  Drive(power, turn);

  // runs all the motors. some are reversed because they are running the opposite way to go forward.
  motor1->run(BACKWARD);
  motor2->run(FORWARD);
  motor3->run(FORWARD);
  motor4->run(BACKWARD);

  // Calculates the Angular Velocity of all motors
  for (int i = 0; i < 4; i++) {
    CalcAngVel(i);
  }
  
  // Prints the Angular Velocity 
  PrintAngVel();
}

// code that sets the speeds of the motors
void Drive(int power, int turn) {
  // Takes the given power and turn and calculates what the mod should be.
  PowerMod(power);
  TurnMod(turn);
  // sets all the motor speeds as the a sum of terms, right now just the power and turn. 
  // The way Power and Turn mods are calculated can be altered in the other methods.
  motor1->setSpeed(PowerMods[0]+TurnMods[0]);
  motor2->setSpeed(PowerMods[1]+TurnMods[1]);
  motor3->setSpeed(PowerMods[2]+TurnMods[2]);
  motor4->setSpeed(PowerMods[3]+TurnMods[3]);
}

// just takes the power and assigns it to the power mod for every motor. Could be room for mapping in the future.
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

// Interrupt functions. They just increment the count for each encoder up by 1
void count0() {EncoderCount[0]++;}
void count1() {EncoderCount[1]++;}
void count2() {EncoderCount[2]++;}
void count3() {EncoderCount[3]++;}

void CalcAngVel(int motorNum) {
  // Motor is 48:1 gearing, with an 8 pole magnet, meaning 1 roation is 384 ticks
  // Checks to see if the sample taking time is up. If yes then it calculates angular velocity
  if (millis() - Time[motorNum] > SampleSize) {
  // Calculates the angular velocity 
  AngVel[motorNum] = (double(EncoderCount[motorNum])/384)/(SampleSize/1000.0);
  // Resets the time for this motor
  Time[motorNum] = millis();
  // Resets encoder count so we don't double count in the future
  EncoderCount[motorNum] = 0;
  }
}

//Prints the Angular Velocity calculated
void PrintAngVel()
{
  Serial.print( AngVel[0]);
  Serial.print("\t");
  Serial.print(AngVel[1]);
  Serial.print("\t");
  Serial.print(AngVel[2]);
  Serial.print("\t");
  Serial.println(AngVel[3]);
}
