import vlc
import os


class VLCRecorder:
    def __init__(self, urls):

        self.instance = vlc.Instance()

        self.urls = urls

        # Creates the VLC Player Object
        self.player = self.instance.media_player_new()

        print os.listdir("ui_components/camera_streaming/video_output")

        onlyfiles = [f for f in os.listdir("ui_components/camera_streaming/video_output/") if os.path.isfile(os.path.join("ui_components/camera_streaming/video_output/", f))]
        self.count = len(onlyfiles)
        print(self.count)

        for i in range(0, len(urls)):
            self.instantiate_media(urls[i], i)

    # makes the broadcasts that we will use to record
    def instantiate_media(self, url, cameraId):
        self.count += 1

        # sout makes the file type to output to
        sout = "#transcode{vcodec=h264,vb=800,width=640,height=480,acodec=mp3,ab=128,channels=2,samplerate=44100}" \
               ":file{mux=mp4,dst=" "video_output/cam" + str(cameraId + 1) + "_" + str(self.count) + ".mp4}"
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