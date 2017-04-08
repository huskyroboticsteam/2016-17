import gps
import time
test = gps.GPS()
latitude = 0
n_s = 0
longitude = 0
e_w = 0
g_speed = 0
while True:
    data = test.getCoords()
    print data