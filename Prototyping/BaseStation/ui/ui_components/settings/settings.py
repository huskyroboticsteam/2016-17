from PyQt4 import QtCore

"""
Operate the settings page in the main ui
Reads from .settings on startup and writes over .settings on shutdown
"""


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

        # Tell the command_api to generate a new map
        result = self.comm.generate_new_map(name, lat, lng)

        # If we generated successfully (user data is validated)
        if result:
            self.main.map_name.setText("")
            self.main.lat.setText("")
            self.main.lng.setText("")

    # Utility function to get the default map name
    def get_map_name(self):
        return self.main.map_val.text()

    # Get the urls that each feed is set to on startup
    def get_camera_urls(self):
        temp = []

        temp.append(self.cam_list[self.main.cam1.currentIndex()])
        temp.append(self.cam_list[self.main.cam2.currentIndex()])
        temp.append(self.cam_list[self.main.cam3.currentIndex()])

        return temp

    # Saves the current state of the settings page except for generation of new map form
    def save(self):
        # Write over the settings file
        f = open(".settings", "w")
        # Write the map name we will open on startup (not validated)
        f.write("default_map=" + str(self.main.map_val.text()) + "\n")

        # Skip the cams= line since the user shouldn't change this in operation
        f.next()

        # Write the currently selected camera for each feed
        f.write("default_cam_1=" + str(self.main.cam1.currentIndex()) + "\n")
        f.write("default_cam_2=" + str(self.main.cam2.currentIndex()) + "\n")
        f.write("default_cam_3=" + str(self.main.cam3.currentIndex()) + "\n")

        f.close()

    def setup(self):
        # Read settings from the settings file
        f = open(".settings", "r")

        # Read in map value
        self.main.map_val.setText(f.next().strip('\n').split("=")[1])

        # Read in the list of cameras and their friendly names
        camStr = f.next().strip('\n').split("=")[1]
        # Cam list alternates friendly name, file location, name...
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


