import vlc
import random


class VLCRecorder:
    def __init__(self, urls):

        self.instance = vlc.Instance()

        self.numbers = []
        self.highEnd = 400000
        self.lowEnd = 5

        self.urls = urls

        # Creates the VLC Player Object
        self.player = self.instance.media_player_new()

        for i in range(0, len(urls)):
            self.instantiate_media(urls[i], i)

    # makes the broadcasts that we will use to record
    def instantiate_media(self, url, cameraId):
        # sout makes the file type to output to
        sout = "#transcode{vcodec=h264,vb=800,width=640,height=480,acodec=mp3,ab=128,channels=2,samplerate=44100}" \
               ":file{mux=mp4,dst=" "cam" + str(cameraId + 1) + "X" + self.create_random() + ".mp4}"
        # makes a "broadcast" to record, with name (filename)
        self.instance.vlm_add_broadcast(str(cameraId), url, sout, 0, None, True, False)

    # destroys than remakes the broadcasts
    def reset_media(self, cameraId):
        self.instance.vlm_del_media(str(cameraId))
        self.instantiate_media(self.urls[cameraId], cameraId)

    # starts the recording
    def start_recording(self, cameraId):
        self.instance.vlm_play_media(str(cameraId))

    # stops the recording
    def stop_recording(self, cameraId):
        self.instance.vlm_stop_media(str(cameraId))
        self.reset_media(cameraId)

    def create_random(self):
        number = random.randint(self.lowEnd, self.highEnd)
        keep_checking = True

        while keep_checking:
            keep_checking = False
            for i in range(0, len(self.numbers)):
                if len(self.numbers) == self.highEnd - self.lowEnd:
                    print("Ran out of filespace")
                    quit("You didn't define the filespace properly")
                if self.numbers[i] == number:
                    number = random.randint(self.lowEnd, self.highEnd)
                    keep_checking = True
                    break

        self.numbers.append(number)
        print(number)
        return str(number)