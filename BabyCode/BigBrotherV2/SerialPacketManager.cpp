/* Communication Protocal
 *  Message begins with bytes {70, 0}
 *  next bytes are {length, checksum}
 *  length refers to number of data bytes after checksum
 *  checksum calculated by adding all data values
 *  next byte is command byte, 20 is drive.  Nothing else implimented yet
 *  next two bytes after drive command is throttle, and turn respectively
 *  0 -> -100%, 127 -> neutral, 255 -> 100%
 *  
 *  if the byte 70 is found anywere in the data, it is to be replaced with
 *  {70, 70}, and the checksum should only include one instance of this 70
 */

#include "SerialPacketManager.h"
#include <SoftwareSerial.h>
#include "Arduino.h"

SerialPacketManager::SerialPacketManager(int baud) {
  Serial1.begin(baud);
}

// attempts to read packets from the serial port for the given
// number of milliseconds, or until all available data has been read
void SerialPacketManager::readSerial(int timeOut) {
  long timer = millis();
  int bytesAvailable = Serial1.available();
  while (bytesAvailable > 0 && millis() - timer < timeOut) {
    byte curByte = Serial1.read();
    bytesAvailable--;
    if (_escaped) {
      _escaped = false;
      switch (curByte) {
        case 0: // beginning of message
          _bufferIndex = 0;
          _checkSum = 0;
          break;
        case 70:
          _bufferArray[_bufferIndex] = curByte;
          _checkSum += curByte;
          _bufferIndex++;
          break;
        case 255:
          _checkSum = _checkSum - _bufferArray[0] - _bufferArray[1];
          if(goodPacket()) {
            byte message[_bufferIndex - 2];
            for(int i=0; i<sizeof(message); i++) {
              message[i] = _bufferArray[i+2];
            }
            onPacketReady(message, sizeof(message));
          }
      }
    }
    else if(curByte == 70) {
      _escaped = true;
    }
    else {
      _bufferArray[_bufferIndex] = curByte;
      _checkSum += curByte;
      _bufferIndex++;
    }
    if (_bufferIndex > 255) {
      _bufferIndex = 255;
    }
  }
}
  
void SerialPacketManager::nextPacket() {
  
}

int  SerialPacketManager::packetsAvailable() {
  
}

// Checks if the buffer contains a good packet
boolean SerialPacketManager::goodPacket() {
  if (_bufferIndex < 2)
    return false;
  byte expectedLength = _bufferArray[0];
  byte expectedCheck = _bufferArray[1];
  return expectedLength == _bufferIndex - 2 && expectedCheck == _checkSum;
}
