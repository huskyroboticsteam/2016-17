#ifndef SerialPacketManager_h
#define SerialPacketManager_h

#include "Arduino.h"
#include "SoftwareSerial.h"
#include "RobotInterface.h"

struct Message {
  byte *data[];
  Message *nextMessage;  
};

class SerialPacketManager {
  public:
    SerialPacketManager(int baud);
    void readSerial(int timeOut);
    void nextPacket();
    int packetsAvailable();
    void (*onPacketReady)(byte data[], int myLength);
  
  private:
    boolean goodPacket();
    byte _bufferArray[255];
    int _bufferIndex = 0;
    boolean _escaped;
    byte _checkSum;
    const byte _ESCAPE = 70;
    const byte _BEGIN = 0;
    const byte _END = 255;
    Message firstMessage;
    Message lastMessage;
};

#endif
