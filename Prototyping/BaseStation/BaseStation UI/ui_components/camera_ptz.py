import urllib
import urllib2
import base64

"""
This module implements a subset of the Messoa IP Camera protocol for panning,
tilting, and zooming.
"""


class PTZCamera:
    """An instance of a Messoa Camera"""

    """
    Initialize a PTZCamera.
    `camera_address` is a string for the address to the camera (IP or symbolic)
    `username` and `password` are the credentials for authenticating with the
    camera's web interface.
    """

    def __init__(self, camera_address, username, password):
        base64_credentials = base64.b64encode("{}:{}".format(username,
                                                             password))
        self._headers = {
            'Cookie': 'pt_speed=100; ipcam_profile=4; tour_index=-1',
            'Authorization': 'Basic {credentials}'.format(
                credentials=base64_credentials)
        }
        self._base_url = "http://{cam_addr}/".format(cam_addr=camera_address)

    """
    Sends a GET request to the camera to the root address `relative_url`
    with the URL arguments `values`
    """

    def _send_data(self, relative_url, values):
        data = list()
        for key, value in values.items():
            data.append("=".join((key, value)))
        url = self._base_url + relative_url + "?" + "&".join(data)
        req = urllib2.Request(url, headers=self._headers)
        response = urllib2.urlopen(req)

    """
    Sends the x and y speeds to the camera. They must be values between
    -100 and 100, otherwise behavior is unknown.
    """

    def set_speeds(self, x_speed, y_speed):
        values = {
            'continuouspantiltmove': '{x_speed},{y_speed}'.format(
                x_speed=x_speed, y_speed=y_speed)
        }
        self._send_data("ptz.cgi", values)

    # print x_speed
    # print y_speed


if __name__ == "__main__":
    import sys
    import time

    camera_ip, username, password = sys.argv[1:]
    cam_instance = PTZCamera(camera_ip, username, password)
    cam_instance.set_speeds(-100, -100)
    time.sleep(5)
    cam_instance.set_speeds(100, 100)
