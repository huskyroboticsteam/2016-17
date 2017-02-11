import gps
import time
test = gps.GPS()
latitude = 0
n_s = 0
longitude = 0
e_w = 0
g_speed = 0
while True:
    data = test.read()
    if data:
        latitude = data[3]
        n_s = data[4]
        longitude = data[5]
        e_w = data[6]
        g_speed = data[7]
    print latitude