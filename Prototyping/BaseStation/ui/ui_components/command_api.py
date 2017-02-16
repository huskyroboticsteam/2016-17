from map import Generator

"""
A utility class that takes in many other objects for cross module updating
"""


class CommandApi:
    def __init__(self, sensor_module):
        self.map = None
        self.sensors = sensor_module

    # Since pygame initialization is strange we need to give it after init
    def feedin_map(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng):
        print self.map
        g = Generator.Generator(self.map.TILE_SIZE, self.map.image_tiles)
        return g.generate_maps(map_name, lat, lng)

    def update_sensors(self, pot, mag, enc_1, enc_2, enc_3, enc_4):
        print
        # TODO: update sensor module

    def update_rover_pos(self, lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec):
        if self.map is not None:
            print

    def send_auto_data(self):
        print
