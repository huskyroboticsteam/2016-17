# -*- coding: utf-8 -*-

import time
import signal
import threading

import sdl2
import sdl2.ext

import camera_ptz

class PTZController:
    def __init__(self, camera_ip, username, password):

        self.x_speed = 0
        self.y_speed = 0
        self.last_x_sent = 0
        self.last_y_sent = 0
        self.camera_instance = camera_ptz.PTZCamera(camera_ip, username, password)
        self._sdl2_update_thread = threading.Thread(target=self._update_sdl2)
        self._sdl2_update_thread.daemon = True
        self._value_lock = threading.Lock()
        self._stopping = False

        # Setup SDL2
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        #sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        self.joystick = sdl2.SDL_JoystickOpen(0)

    def _update_sdl2(self):
        while not self._stopping:
            with self._value_lock:
                for event in sdl2.ext.get_events():
                    if event.type == sdl2.SDL_KEYDOWN:
                        print(sdl2.SDL_GetKeyName(event.key.keysym.sym).lower())
                    elif event.type == sdl2.SDL_JOYAXISMOTION:
                        #print(event.jaxis.which, "axis motion:", "-", "axis:", event.jaxis.axis, "value:", event.jaxis.value)
                        #if abs(event.jaxis.value) > 32768 * 0.9:
                        #    target_speed = (event.jaxis.value / abs(event.jaxis.value)) * 75
                        if abs(event.jaxis.value) > 32768 * 0.3:
                            target_speed = (event.jaxis.value / abs(event.jaxis.value)) * 50
                        else:
                            target_speed = 0

                        if event.jaxis.axis == 1:
                            self.y_speed = target_speed
                            #self.y_speed = int(round(event.jaxis.value / 32768.0, 1)*75)
                        elif event.jaxis.axis == 0:
                            self.x_speed = target_speed
                            #self.x_speed = int(round(event.jaxis.value / 32768.0, 1)*75)
                    elif event.type == sdl2.SDL_JOYBALLMOTION:
                        print(event.jball.which, "ball motion", "-", "ball:", event.jball.ball, "xrel:", event.jball.xrel, "yrel:", event.jball.yrel)
                    elif event.type == sdl2.SDL_JOYHATMOTION:
                        print(event.jhat.which, "hat motion", "-", "hat:", event.jhat.hat, "value:", event.jhat.value)
                    elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                        print(event.jbutton.which, "button down", "-", "button:", event.jbutton.button, "state:", event.jbutton.state)
                    elif event.type == sdl2.SDL_JOYBUTTONUP:
                        print(event.jbutton.which, "button up", "-", "button:", event.jbutton.button, "state:", event.jbutton.state)
                    elif event.type == sdl2.SDL_JOYDEVICEADDED:
                        print(event.jdevice.which, "joystick added")
                        self.joystick = sdl2.SDL_JoystickOpen(0)
                    elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                        print(event.jdevice.which, "joystick removed")
            time.sleep(1.0 / 120.0)

    def _send_speeds(self):
        while not self._stopping:
            with self._value_lock:
                if self.last_x_sent != self.x_speed or self.last_y_sent != self.y_speed:
                    print self.x_speed, self.y_speed
                    #if (self.x_speed != self.last_x_sent) or (self.y_speed != self.last_y_sent):
                    #    self.camera_instance.set_speeds(0, 0)
                    self.camera_instance.set_speeds(self.x_speed, self.y_speed)
                    self.last_x_sent = self.x_speed
                    self.last_y_sent = self.y_speed
            time.sleep(1.0 / 50.0)

    def start_loops(self):
        self._sdl2_update_thread.start()
        self._send_speeds()

    def stop_loops(self, *args):
        with self._value_lock:
            self._stopping = True
        self._sdl2_update_thread.join()
        
if __name__ == '__main__':
    import sys
    camera_ip, username, password = sys.argv[1:]
    controller = PTZController(camera_ip, username, password)
    signal.signal(signal.SIGINT, controller.stop_loops)
    signal.signal(signal.SIGTERM, controller.stop_loops)
    controller.start_loops()
