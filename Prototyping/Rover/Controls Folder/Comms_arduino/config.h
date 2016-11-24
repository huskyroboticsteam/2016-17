#ifndef _CONFIG_H_
#define _CONFIG_H_

// MOTOR CONTROL CONSTANTS //
#define TALON_NEUTRAL_FREQUENCY 1500

#define THROTTLE_PIN 7
#define TURN_PIN 8
#define AUTOPILOT_PIN 9

#define THROTTLE_MIN 1085
#define THROTTLE_MAX 1927

#define TURN_MIN 1094
#define TURN_MAX 1921

#define AUTOPILOT_OFF 1086
#define AUTOPILOT_ON 1931


// ARM CONTROL CONSTANTS //
#define ARM_TALON_NEUTRAL_FREQUENCY 2000


#define ARM_SPEED 200

// CAMERAS //

#define EYE_OF_SAURON 10


// ETHERNET COMMUNICATION CONSTANTS //
#define UDP_PORT         8888
#define DESTINATION_PORT 8887
#define TIMEOUT          500

// send/recieve structs

struct sendData {
  
};

struct recieveData {
  short a;
  short b;
};

// SERIAL COMMUNICATION CONSTANTS //
#define BAUD_RATE 9600

// STEERING EQUATION CONSTANTS //
#define POTENTIOMETER A6 
#define VERTICAL_WHEEL_SEPARATION  27.6 // in
#define LATERAL_WHEEL_SEPARATION   22.4 // in
#define MAX_TURN_ANGLE 45 // degrees
#define TUNING_CONSTANT 1 // constant for error correction

// GPS CONSTANTS //
#define GPS_RX A3
#define GPS_TX A2
#define VALID_POS_TIMEOUT = 2000;

// First byte is all stop, second byte is pot stop, 
// next two bytes of the packet is the angle, second pair of bytes is the speed, 
// the next 14 bytes are arm controls, the last 4 bytes are for camera movement

#endif  // _CONFIG_H_

