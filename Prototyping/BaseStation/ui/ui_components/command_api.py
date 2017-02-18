from map import Generator


class CommandApi:
    def __init__(self):
        self.map = None

    def feedin_map(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng):
        print self.map
        g = Generator.Generator(self.map.TILE_SIZE, self.map.image_tiles)
        return g.generate_maps(map_name, lat, lng)
