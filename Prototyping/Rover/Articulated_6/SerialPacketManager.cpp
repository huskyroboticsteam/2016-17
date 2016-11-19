#include "SerialPacketManager.h"
#include <SoftwareSerial.h>
#include "Arduino.h"

SerialPacketManager::SerialPacketManager(int rxPin, int txPin, int baud) : _mySerial(SoftwareSerial(rxPin,txPin)) {
  _mySerial.begin(baud);
}

// attempts to read packets from the serial port for the given
// number of milliseconds, or until all available data has been read
void SerialPacketManager::readSerial(int timeOut) {
  long timer = millis();
  int bytesAvailable = _mySerial.available();
  while (bytesAvailable > 0 && millis() - timer < timeOut) {
    byte curByte = _mySerial.read();
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
//          for(int i=0; i < _bufferIndex; i++) {
//            Serial.print(_bufferArray[i]);
//            Serial.print(" ");
//          }
//          Serial.println();
          if(goodPacket()) {
            byte message[_bufferIndex - 2];
            for(int i=0; i<sizeof(message); i++) {
              message[i] = _bufferArray[i+2];
//              for (int i=0; i<sizeof(message); i++) {
//                Serial.print(message[i]);
//                Serial.print(" ");
//              }
//              Serial.println();
            }
            onPacketReady(message, sizeof(message));
            /*if (onPacketReady != NULL) {
              onPacketReady(message, sizeof(message));
            } else {
              Serial.println("null!");
            }*/
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
