
class Settings:
    def __init__(self, ui, command_api):
        self.comm = command_api
        self.main = ui

        self.main.generate.clicked.connect(self.generate_new_map)

        self.setup()

    def generate_new_map(self):
        name = self.main.map_name
        lat = self.main.lat
        lng = self.main.lng
        self.comm.generate_new_map(name, lat, lng)

    def get_map_name(self):
        return self.main.map_val.text()

    def setup(self):
        f = open(".settings", "r")
        self.main.map_val.setText(f.next().strip('\n').split("=")[1])
        f.close()


