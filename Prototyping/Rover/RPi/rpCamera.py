from picamera import PiCamera
from time import sleep, strftime
import io
import struct
import socket
import numpy as np

class piCamera :
    def __init__(self):
        #Picamera setup
        self.camera = PiCamera()
        self.camera.resolution = (640,480)
        self.camera.framerate = 24
        #socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('192.168.1.40', 1555))
        self.sender = self.socket.makefile('wb')

    #get time for filenames   
    def get_time(self):
        return strftime("%a %b %d %Y %H:%M:%S")

    #take one shot and store it locally   
    def one_shot(self):
        self.camera.capture(self.get_time() + ".jpg")
        sleep(5)

    #take (shot) shots and store them locally    
    def mult_shot(self, shot):
        for i in range (shot):
            self.camera.capture(self.get_time() + ".jpg")
            sleep(5)

    def start_p(self):
        self.camera.start_preview()

    def end_p(self):
        self.camera.stop_preview()

    def kill(self):
        self.camera.close()

    #outputs continuous images to target
    def pic_out(self, imagetype):
        #because the camera takes shots so rapidly
        #we use an io stream to handle image storage
        stream = io.BytesIO()
        #this will go forever until you break it!
        for foo in self.camera.capture_continuous(stream, imagetype):
            #send size of image first
            self.sender.write(struct.pack('<L', stream.tell()))
            self.sender.flush()
            #send image
            stream.seek(0)
            self.sender.write(stream.read())
            #end clause here!!!!
            '''if foo:
                break'''
            #reset stream
            stream.seek(0)
            stream.truncate()

    #outputs video from piCamera
    def vid_out(self):
        #use socket file to send video to target 
        self.camera.start_recording(self.sender, format='h264')
        #end clause here!!!!
        #Ex: self.camera.wait_recording(60)
        self.camera.stop_recording()

cam = piCamera()
cam.pic_out('jpeg')
print "done"
