
class Settings:
    def __init__(self, ui, command_api):
        self.comm = command_api
        self.main = ui

        self.main.generate.clicked.connect(self.generate_new_map)

        self.setup()

    def generate_new_map(self):
        name = self.main.map_name.text()
        lat = self.main.lat.text()
        lng = self.main.lng.text()
        result = self.comm.generate_new_map(name, lat, lng)

        # If we generated successfully
        if result:
            self.main.map_name.setText("")
            self.main.lat.setText("")
            self.main.lng.setText("")

    def get_map_name(self):
        return self.main.map_val.text()

    def save(self):
        f = open(".settings", "w")
        f.write("default_map=" + str(self.main.map_val.text()) + "\n")
        f.close()

    def setup(self):
        f = open(".settings", "r")
        self.main.map_val.setText(f.next().strip('\n').split("=")[1])
        f.close()


