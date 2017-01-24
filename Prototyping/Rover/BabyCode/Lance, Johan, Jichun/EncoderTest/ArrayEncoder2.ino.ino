//These variables need to stay out of the fuction because if they are in they get reset and we don't want that
const int SAMPLE_SIZE = 1000;
const byte PIN = 18;
double angVelArray[4];
unsigned long currTime = millis();
volatile int ticksCount = 0;

void setup() {
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(PIN), countUpdate, CHANGE);
}

void loop() {
//  for (int i = 0; i < 4; i++) {
//    angVelArray[i] = calcAngVel();
//  }
  if (millis() - currTime > SAMPLE_SIZE) {
    angVelArray[0] = calcAngVel();
    Serial.println(angVelArray[0]);
    currTime = millis();
  }
}

// ISR: updates ticksCount
void countUpdate() {
  ticksCount++;
}

double calcAngVel() {
  // Motor is 48:1 gearing, with an 8 pole magnet, meaning 1 roation is 384 ticks
  // Some local variables for the function
  //Checks to see if the sample taking time is up. If yes then it calculates angular velocity
  double angVel = (double(ticksCount)/384)/(SAMPLE_SIZE/1000.0);
  // ticksCount = 0;
  return angVel;
}

