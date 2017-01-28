__author__ = 'Trevor'

from Prototyping.BaseStation.Examples.OldGUI.codeToIntegrate.Nathan import nextcamera

camOne = "rtsp://192.168.1.12:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
#camThree = "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"

urls1 = [camOne]
urls2 = [camTwo]

if __name__ == '__main__':
    nextcamera.main(urls1, 520, 300, 0, 400000)