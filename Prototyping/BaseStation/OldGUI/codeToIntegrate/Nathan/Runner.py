import nextcamera

camOne = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.20:554/user=admin&password=&channel=1&stream=0.sdp"
camThree = "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"

urls = [camOne]

if __name__ == '__main__':
    nextcamera.main(urls, 520, 300, 0, 400000)