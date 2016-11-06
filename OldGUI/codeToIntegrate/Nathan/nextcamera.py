import sys
import pygtk
import gtk
import gobject
import vlc
import random

pygtk.require("2.0")

sizeX = 0
sizeY = 0

gobject.threads_init()


class ButtonWrap:
    # connects our buttons to the gtk lib
    # id's are unique to each button
    # sets the button to false so it doesn't record
    def __init__(self, button_id):
        self.button = gtk.Button()
        self.id = button_id
        self.recording = False


class VLCWidget(gtk.DrawingArea):
    def __init__(self, vlc_i):
        gtk.DrawingArea.__init__(self)

        # Creates the VLC Player Object
        self.player = vlc_i.media_player_new()
        self.id = ""
        self.url = ""

        # Give the Windows ID to VLC
        def handle_embed(*args):
            if sys.platform == 'win32':
                gobject.idle_add(self.set_window, self.window)
            else:
                gobject.idle_add(self.set_xwindow, self.window)
            return True

        # Once widget event map is run it will call the function handle_embed
        self.connect("map", handle_embed)

        # Set initial window size of widget
        if sizeX != 0 and sizeY != 0:
            self.set_size_request(sizeX, sizeY)
        else:
            self.set_size_request(320, 200)

    def set_window(self, window):
            self.player.set_hwnd(window.handle)

    def set_xwindow(self, window):
            self.player.set_xwindow(window.xid)


class VLCRecorder:
    def __init__(self, low_end, high_end):

        self.instance = vlc.Instance()

        # Creates the VLC Player Object
        self.player = self.instance.media_player_new()
        self.numbers = []
        self.lowEnd = low_end
        self.highEnd = high_end

    # makes the broadcasts that we will use to record
    def instantiate_media(self, url, filename):
        # sout makes the file type to output to
        sout = "#transcode{vcodec=h264,vb=800,width=640,height=480,acodec=mp3,ab=128,channels=2,samplerate=44100}" \
               ":file{mux=mp4,dst=" "cam" + filename + "X" + self.create_random() + ".mp4}"
        # makes a "broadcast" to record, with name (filename)
        self.instance.vlm_add_broadcast(filename, url, sout, 0, None, True, False)

    # destroys than remakes the broadcasts
    def reset_media(self, url, filename):
        self.instance.vlm_del_media(filename)
        self.instantiate_media(url, filename)

    # starts the recording
    def start_recording(self, filename):
        self.instance.vlm_play_media(filename)

    # stops the recording
    def stop_recording(self, filename):
        self.instance.vlm_stop_media(filename)

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


class MainUI:
    def __init__(self, urls, low_end, high_end):
        """makes to window for display"""
        self.window = gtk.Window()
        # sets the icon and name of the window
        self.window.set_title("Dope Cameras")
        self.window.set_icon_from_file("icon.png")

        # makes the "box" objects for the code
        self.vertBox = gtk.VBox()
        self.topHorBox = gtk.HBox(homogeneous=True)
        self.bottomHorBox = gtk.HBox(homogeneous=True)

        self.window.add(self.vertBox)
        # adds the boxes vertically then horrizontally
        self.vertBox.add(self.topHorBox)
        # for the camera display
        self.vertBox.add(self.bottomHorBox)
        # for the buttons

        self.urls = urls
        self.buttons = []
        self.recorder = VLCRecorder(low_end, high_end)

        # Initialize the initial stream and pack into window
        self.widgets = create_widgets(self.urls)
        for i in range(0, len(self.urls)):
            self.topHorBox.pack_start(self.widgets[i], expand=True)

        for i in range(0, len(self.urls)):
            self.recorder.instantiate_media(self.urls[i], str(i + 1))

        # Connect all buttons to the callback function
        for i in range(0, len(self.urls)):
            button_wrap = ButtonWrap(i)
            button_wrap.button.set_label("Record Feed " + str(i + 1))
            button_wrap.button.connect("clicked", self.button_clicked)
            self.bottomHorBox.add(button_wrap.button)
            self.buttons.append(button_wrap)

        # Get the Main Window, and connect the "destroy" event
        if self.window:
            # Shows Window and all children objects
            self.window.show_all()
            # Closes infinite loop on pressing exit button (destroys main window)
            self.window.connect("destroy", gtk.main_quit)

    def button_clicked(self, button):
        for i in range(0, len(self.buttons)):
            if self.buttons[i].button == button:
                record_toggle(self.buttons[i], self.urls, self.recorder)


def create_widgets(urls):
    # Empty list to hold vlc widgets
    widgets = []

    # Check if the instances and url lengths match, if not there is a critical error
    for i in range(0, len(urls)):
        instance = vlc.Instance()
        vlc_widget = VLCWidget(instance)
        vlc_widget.id = i
        vlc_widget.url = urls[i]
        player = vlc_widget.player
        player.set_media(instance.media_new(urls[i], ":network-caching=300"))
        gobject.idle_add(play, player)
        widgets.append(vlc_widget)

    return widgets


def play(player):
    player.play()


def record_toggle(button_wrap, urls, recorder):
    # determines when to record

    button = button_wrap.button
    button_id = button_wrap.id
    is_recording = button_wrap.recording

    # id is used to determine which button and which camera is used
    if not is_recording:
        button.set_label("Stop Recording Feed " + str(button_id + 1))
        recorder.start_recording(str(button_id + 1))
        button_wrap.recording = True
    elif is_recording:
        button.set_label("Record Feed " + str(button_id + 1))
        button_wrap.recording = False
        recorder.stop_recording(str(button_id + 1))
        recorder.reset_media(urls[button_id], str(button_id + 1))


# Main Function
def main(urls, x, y, low_end, high_end):

    global sizeX
    sizeX = x
    global sizeY
    sizeY = y

    # Pass all URL RTSP parameters and random number generator bounds to the UI for initialization
    MainUI(urls, low_end, high_end)

    # Start the UI loop
    gtk.main()
