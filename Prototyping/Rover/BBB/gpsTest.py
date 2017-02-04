import gps
import time
gps = gps.GPS()
while True:
    print gps.read()
    time.sleep(1)