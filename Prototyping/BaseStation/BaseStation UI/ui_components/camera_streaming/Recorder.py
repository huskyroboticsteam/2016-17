import vlc
import os


class VLCRecorder:
    def __init__(self, url, cameraId):

        self.url = url
        self.cameraId = cameraId
        urlA = url.split("Profile")
        urlA[1] = str(int(urlA[1]) - 1)
        self.url = urlA[0] + urlA[1]
        print self.url
        self.instantiate_media()

    # makes the broadcasts that we will use to record
    def instantiate_media(self):
        onlyfiles = [f for f in os.listdir("ui_components/camera_streaming/video_output/") if
                     os.path.isfile(os.path.join("ui_components/camera_streaming/video_output/", f))]
        self.count = len(onlyfiles)
        # Creates the VLC Player Object
        cmd3 = "--sout=#transcode{vencoder=libavformat,vcodec=h264}:std{access=file,mux=mp4,dst=ui_components/camera_streaming/video_output/cam" + str(
            self.cameraId + 1) + "_" + str(self.count) + ".mp4}"
        self.instance = vlc.Instance(cmd3)
        self.player = self.instance.media_player_new()

        self.player.set_media(self.instance.media_new(self.url, ":network-caching=300"))

    # destroys than remakes the broadcasts
    def reset_media(self):
        self.instantiate_media()

    # starts the recording
    def start_recording(self):
        self.player.play()

    # stops the recording
    def stop_recording(self):
        self.player.stop()
        self.reset_media()