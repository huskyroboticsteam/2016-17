//#include <AFMotor.h>
//
////AF_DCMotor motor(2, MOTOR12_64KHZ); // create motor #2, 64KHz pwm
//AF_DCMotor *motor[4];
//void setup() {
//  for (int i=0; i<4; i++) {
//    motor[i] = new AF_DCMotor(i+1, MOTOR12_64KHZ);
//    motor[i]->setSpeed(200);
//  }
//Serial.begin(9600); // set up Serial library at 9600 bps
//Serial.println("Motor test!");
//}
//
//void loop() {
//Serial.print("tick");
//for (int i=0; i<4; i++) {
//  motor[i]->run(FORWARD);
//}
//delay(1000);
//
//Serial.print("tock");
//for (int i=0; i<4; i++) {
//  motor[i]->run(BACKWARD);
//}
//delay(1000);
//
//Serial.print("tack");
//for (int i=0; i<4; i++) {
//  motor[i]->run(RELEASE);
//}
//delay(1000);
//}

