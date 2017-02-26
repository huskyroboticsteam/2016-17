import sdl2


class SDLInstance:
    max_axis_value = 2 ** 15

    # Initialises PySDL2 and the variables to store the joystick data
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

        self.joystick_axis = []
        self.joystick_ball = []
        self.joystick_hat = []
        self.joystick_button = []

    def init_joy_vars(self, joy_num):
        self.joystick_axis = []
        self.joystick_ball = []
        self.joystick_hat = []
        self.joystick_button = []

        for i in range(joy_num):
            current_joystick = sdl2.SDL_JoystickOpen(i)
            axis_num = sdl2.SDL_JoystickNumAxes(current_joystick)
            ball_num = sdl2.SDL_JoystickNumBalls(current_joystick)
            hat_num = sdl2.SDL_JoystickNumHats(current_joystick)
            button_num = sdl2.SDL_JoystickNumButtons(current_joystick)

            self.joystick_axis.append([])
            for j in range(axis_num):
                self.joystick_axis[i].append(0)

            self.joystick_ball.append([])
            for j in range(ball_num):
                self.joystick_ball[i].append([0, 0]);

            for j in range(hat_num):
                self.joystick_hat.append(0);    # [[direction]]

            self.joystick_button.append([]);
            for j in range(button_num):
                self.joystick_button[i].append(0)   # [button1, button2, button3, ...]

    # Takes the joystick input and stores in variables
    def update_sdl2(self, joy_num):
        for event in sdl2.ext.get_events():
            # print "Joystick", event.jdevice.which

            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.joystick_axis[event.jaxis.which][event.jaxis.axis] = event.jaxis.value
                print self.joystick_axis
                # print self.joystick_axis

            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.joystick_ball[event.jball.which][event.jball.ball] = [event.jball.xrel, event.jball.yrel]
                # print self.joystick_ball

            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.joystick_hat[event.jhat.which] = event.jhat.value
                # print self.joystick_hat

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.joystick_button[event.jbutton.which][event.jbutton.button] = event.jbutton.state
                # print self.joystick_button

            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.joystick_button[event.jbutton.which][event.jbutton.button] = event.jbutton.state
                # print self.joystick_button

            elif event.type == sdl2.SDL_JOYDEVICEADDED:

                # sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
                # for i in range(sdl2.SDL_NumJoysticks()):
                #    sdl2.SDL_JoystickOpen(i)

                self.init_joy_vars(sdl2.SDL_NumJoysticks())

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.init_joy_vars(sdl2.SDL_NumJoysticks())
