from map import Generator, Utility

class CommandApi:
    def __init__(self, sensor_module):
        self.map = None
        self.sensors = sensor_module # make this a class variable

    def feedin_map(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng, tile_size, api, zoom15, zoom16, zoom17, zoom18, zoom19):
        arr = [zoom15, zoom16, zoom17, zoom18, zoom19]
        g = Generator.Generator(tile_size, api, arr)
        return g.generate_maps(map_name, lat, lng)

    def update_rover_pos(self, lat, lng):

        # Hopefully won't cause flickering
        if self.map is not None:
            marks = self.map.markers

            # Clear the rover marker
            for i in range(0, len(marks)):
                if marks[i].rover:
                    self.map.remove_marker(i)

            # Re add the rover at the new position
            self.map.add_rover(lat, lng)


# takes in an array of markers
def send_auto_data(comms, markers):

    # Don't send the data again if we are in auto mode
    if comms.auto is False:
        comms.open_tcp()
        for i in range(0, len(markers)):
            if i == len(markers) - 1:
                lat = markers[i].coordX.toAscii()
                long = markers[i].coordY.toAscii()
                lat = float(lat)
                long = float(long)
                print lat
                print long
                comms.send_auto_mode(False, lat, long)
            else:
                lat = markers[i].coordX.toAscii()
                long = markers[i].coordY.toAscii()
                lat = float(lat)
                long = float(long)
                comms.send_auto_mode(True, lat, long)
        comms.auto = True
        comms.close_tcp()
    else:
        comms.auto = False

