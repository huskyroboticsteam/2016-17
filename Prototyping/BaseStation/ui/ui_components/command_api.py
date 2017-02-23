from map import Generator, Utility


class CommandApi:
    def __init__(self, sensor_module):
        self.map = None
        self.sensors = sensor_module #make this a class variable

    def feedin_map(self, map):
        self.map = map

    def generate_new_map(self, map_name, lat, lng):
        g = Generator.Generator(self.map.TILE_SIZE, self.map.image_tiles)
        return g.generate_maps(map_name, lat, lng)

    def update_sensors(self, pot, mag, enc_1, enc_2, enc_3, enc_4):
        dictionary = {"Potentiometer": pot, "Magnetometer": mag, "Encoder 1": enc_1,
                      "Encoder 2": enc_2, "Encoder 3": enc_3, "Encoder 4": enc_4}
        self.sensors.update_ui(dictionary)

    def update_rover_pos(self, lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec):
        lat = Utility.convertToDecimal(lat_deg, lat_min, lat_sec)
        lng = Utility.convertToDecimal(lng_deg, lng_min, lng_sec)

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
    else:
        comms.auto = False

