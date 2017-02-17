
import serial
import Adafruit_BBIO.UART as UART
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)


class GPS:
    def __init__(self):
        #This sets up variables for useful commands.
        #This set is used to set the rate the GPS reports
        UPDATE_200_msec=  "$PMTK220,200*2C\r\n" #Update Every 200 Milliseconds
        #This set is used to set the rate the GPS takes measurements
        MEAS_200_msec= "$PMTK300,200,0,0,0,0*2F\r\n"  #Meaure 5 times a second
        #Commands for which NMEA Sentences are sent
        GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"#Send GPRMC AND GPGGA Sentences
        #reduces the number of senteces that are considered
        #sets the speed of the reporting so it is not too fast
        ser.write(GPRMC_GPGGA)
        sleep(1)
        ser.write(MEAS_200_msec)
        sleep(1)
        ser.write(UPDATE_200_msec)
        sleep(1)
        ser.flushInput()
        ser.flushOutput()
        
        #this is where you write the commands you want to give the NMEA sentences
        #to your serial object from earlier object.write(command) put sleep command after
        
    def read(self):
        try:
            #flush twice to make sure nothing is clogged
            ser.flushInput()
            ser.flushInput()
            while ser.inWaiting() == 0:
                pass
            NMEA = ser.readline()
            Narray = NMEA.split(",")
            if (Narray[0])[-3:] == 'RMC':
                    return Narray
        except AttributeError:
            return -1
    
    # returns coordinates of current location in an array [lat, long]
    # negative lat corresponds to S direction; negative long corresponds to W
    def getCoords(self){
        info = self.read()
        try (info != None):
            lat = info[3]
            latDir = info[4]
            lon = info[5]
            longDir = info[6]
            coords = []
            if (latDir == 'S'):
                coords.append(lat * -1)
            else:
                coords.append(lat)
            if(longDir == 'W'):
                coords.append(lon * -1)
            else:
                coords.append(lon)
            return coords
        except:
            self.getCoords()
            
