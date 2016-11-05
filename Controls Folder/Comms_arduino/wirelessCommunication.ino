// All Functions for Wireless Communication //
#include "Arduino.h"
#include "config.h"
#include <Ethernet.h>
#include <EthernetUdp.h>

void initializeWirelessCommunication()
{
    Ethernet.begin(MAC_ADDRESS, IP);
    Udp.begin(UDP_PORT);
    timeLastPacket = millis();
}

void receiveWirelessData()
{
    networkStatus = parseWirelessData();
}

void sendWirelessData() {
  
}

bool parseWirelessData()
{
    int packetSize = Udp.parsePacket();
    Serial.print("packetSize: ");
    Serial.println(packetSize);
    Udp.read((byte *) &recievedPacket, sizeof recievedPacket);
    Serial.println(recievedPacket.throttle);
    Serial.println(recievedPacket.turn);
    Serial.println(recievedPacket.autoPilot);
    throttle = recievedPacket.throttle;
    turn = recievedPacket.turn;
    autoPilot = recievedPacket.autoPilot;
    return true;
}

bool timeoutCheck()
{
    if(millis() - timeLastPacket >= TIMEOUT) {
      throttle = 0;
      turn = 0;
      autoPilot = false;
      return true;
    }
    return false;
}

