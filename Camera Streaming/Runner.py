import UI

camOne = "rtsp://192.168.1.15:554/user=admin&password=&channel=1&stream=0.sdp"
camTwo = "rtsp://192.168.1.20:554/user=admin&password=&channel=1&stream=0.sdp"
camThree = "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"

# Can use any video file you have laying around. Change to linux paths if using linux.
test = "C:\\money.mp4"

urls = [test]

if __name__ == '__main__':

    # List of urls to play in the UI, width and height of each video container
    UI.main(urls, 520, 300)