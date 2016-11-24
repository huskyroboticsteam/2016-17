import nextcamera

camOne = "rtsp://192.168.1.12:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
camThree = "rtsp://192.168.1.13:554/user=admin&password=&channel=1&stream=0.sdp"

urls1 = [camOne]
urls2 = [camTwo]
urls3 = [camThree]

if __name__ == '__main__':
    nextcamera.main(urls3, 520, 300, 0, 400000)