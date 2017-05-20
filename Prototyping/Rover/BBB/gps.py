
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
        # clears the debugging file
        open('gps.txt', 'w').close()
        
        # this is where you write the commands you want to give the NMEA sentences
        # to your serial object from earlier object.write(command) put sleep command after
        
    def read(self):
        try:
            # flush twice to make sure nothing is clogged
            ser.flushInput()
            ser.flushInput()
            while ser.inWaiting() == 0:
                pass
            NMEA = ser.readline()
            Narray = NMEA.split(",")
            if (Narray[0])[-3:] == 'GGA':
                    return Narray
        except AttributeError:
            return -1
    
    # returns coordinates of current location in tuple (lat, long)
    # negative lat corresponds to S direction; negative long corresponds to W
    def getCoords(self):
        info = self.read()
        try:
            if info is not None:
                lat = self.rawGPStodegGPS(info[2])
                print "================================================================"
                print lat
                latDir = info[3]
                lon = self.rawGPStodegGPS(info[4])
                print lon
                longDir = info[5]
                if (latDir == 'S'):
                    lat = -lat
                if(longDir == 'W'):
                    lon = -lon
                print (lat, lon)
                print "================================================================"
                # logs fo debugging
                with open("gps.txt", "a") as myfile:
                    myfile.write(str((lat,lon)) + '\n')
                return lat, lon
        except:
            return self.getCoords()

    # TODO: check this is getting the right value
    def rawGPStodegGPS(self, val):
        gpsplit = val.split(".")
        deg = (gpsplit[0])[:-2]
        min1 = (gpsplit[0])[-2:]
        min2 = gpsplit[1]
        min = min1 + "." +  min2
        return float(deg) + (float(min)/60)

