from map import Generator, Utility
import comms_update

class CommandApi:
    def __init__(self, sensor_module):
        self.map = None
        self.sensors = sensor_module #make this a class variable

    def feedin_map(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng):
        print self.map
        g = Generator.Generator(self.map.TILE_SIZE, self.map.image_tiles)
        return g.generate_maps(map_name, lat, lng)


    def update_sensors(self, pos, mag, enc_1, enc_2, enc_3, enc_4):
        print
        # TODO: update sensor module


    def update_rover_pos(self, lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec):
        if self.map is not None:
            print


# takes in an array of markers
def send_auto_data(markers):
    for marker in markers:
        lat = Utility.decdeg2dms(marker.coorX)
        long = Utility.decdeg2dms(marker.coorY)
        comms_update.send_auto_mode(lat[0], lat[1], lat[2], long[0], long[1], long[2])

