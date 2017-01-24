import serial
import Adafruit_BBIO.UART as UART
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)


class GPS:
    def __init__(self):
        #This sets up variables for useful commands.
        #This set is used to set the rate the GPS reports
        UPDATE_10_sec=  "$PMTK220,10000*2F\r\n" #Update Every 10 Seconds
        UPDATE_5_sec=  "$PMTK220,5000*1B\r\n"   #Update Every 5 Seconds  
        UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"   #Update Every One Second
        UPDATE_200_msec=  "$PMTK220,200*2C\r\n" #Update Every 200 Milliseconds
        #This set is used to set the rate the GPS takes measurements
        MEAS_10_sec = "$PMTK300,10000,0,0,0,0*2C\r\n" #Measure every 10 seconds
        MEAS_5_sec = "$PMTK300,5000,0,0,0,0*18\r\n"   #Measure every 5 seconds
        MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"   #Measure once a second
        MEAS_200_msec= "$PMTK300,200,0,0,0,0*2F\r\n"  #Meaure 5 times a second
        #Set the Baud Rate of GPS
        BAUD_57600 = "$PMTK251,57600*2C\r\n"          #Set Baud Rate at 57600
        BAUD_9600 ="$PMTK251,9600*17\r\n"             #Set 9600 Baud Rate
        #Commands for which NMEA Sentences are sent
        GPRMC_ONLY= "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n" #Send only the GPRMC Sentence
        GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"#Send GPRMC AND GPGGA Sentences
        SEND_ALL ="$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" #Send All Sentences
        SEND_NOTHING="$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" #Send Nothing
        ser.write(MEAS_200_msec)
        sleep(1)
        ser.write(GPRMC_GPGGA)
        sleep(1)
        ser.flushInput()
        ser.flushOutput()
        
        #this is where you write the commands you want to give the NMEA sentences
        #to your serial object from earlier object.write(command) put sleep command after
        
    def read(self):
        #flush twice to make sure nothing is clogged
        ser.flushInput()
        ser.flushInput()
        while ser.inWaiting() == 0:
            pass
        NMEA = ser.readline()
        print NMEA
        Narray = NMEA.split(",")
        #sentences can be found by the leading term
        if Narray[0] == '$GPGGA':
            pass
        if Narray[0] == '$GPRMC':
            self.Latitude = Narray[3]
            self.n_s = Narray[4]
            self.longitude = Narray[5]
            self.e_w = Narray[6]
            self.g_speed = Narray[7]


test = GPS()
while 1:
    test.read()
    print test.Latitude