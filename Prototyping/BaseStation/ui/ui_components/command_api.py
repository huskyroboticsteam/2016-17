from map import Generator


class CommandApi:
    def __init__(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng):
        g = Generator.Generator(self.map.TILE_SIZE, self.map.image_tiles)
        g.generate_maps(map_name, lat, lng)
