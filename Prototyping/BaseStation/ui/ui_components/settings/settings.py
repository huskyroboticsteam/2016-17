from PyQt4 import QtCore


class Settings:
    def __init__(self, ui, command_api):
        self.comm = command_api
        self.main = ui

        self.cam_list = []

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

    def get_camera_urls(self):
        temp = []

        temp.append(self.cam_list[self.main.cam1.currentIndex()])
        temp.append(self.cam_list[self.main.cam2.currentIndex()])
        temp.append(self.cam_list[self.main.cam3.currentIndex()])

        return temp

    def save(self):
        # Write over the settings file
        f = open(".settings", "w")
        f.write("default_map=" + str(self.main.map_val.text()) + "\n")

        output = ""
        for i in range(0, len(self.cam_list)):
            output += self.main.cam1.itemText(i)
            output += ","
            output += self.cam_list[i]
            if i != len(self.cam_list) - 1:
                output += ","

        f.write("cams=" + output + "\n")

        f.write("default_cam_1=" + str(self.main.cam1.currentIndex()) + "\n")
        f.write("default_cam_2=" + str(self.main.cam2.currentIndex()) + "\n")
        f.write("default_cam_3=" + str(self.main.cam3.currentIndex()) + "\n")

        f.close()

    def setup(self):
        # Read settings from the settings file
        f = open(".settings", "r")
        # Read in map value
        self.main.map_val.setText(f.next().strip('\n').split("=")[1])

        camStr = f.next().strip('\n').split("=")[1]
        camList = camStr.split(",")

        list = QtCore.QStringList()

        for i in range(0, len(camList)):
            if i % 2 == 0:
                # Add the names of the cameras
                list.append(camList[i])
            else:
                # Add the URLS to the list
                self.cam_list.append(camList[i])

        # Add the options to the selection boxes
        self.main.cam1.addItems(list)
        self.main.cam2.addItems(list)
        self.main.cam3.addItems(list)

        # Read in default indices of the select boxes
        self.main.cam1.setCurrentIndex(int(f.next().strip('\n').split("=")[1]))
        self.main.cam2.setCurrentIndex(int(f.next().strip('\n').split("=")[1]))
        self.main.cam3.setCurrentIndex(int(f.next().strip('\n').split("=")[1]))

        f.close()


