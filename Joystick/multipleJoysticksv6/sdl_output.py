import sdl2


class SDLInstance:
    max_axis_value = 2 ** 15

    # Initialises PySDL2 and the variables to store the joystick data
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

        self.joystick_number = sdl2.SDL_NumJoysticks()

        self.which_joystick = None
        self.joystick_axis = []

        self.which_joystick_ball = None
        self.joystick_ball = None
        self.joystick_ball_x_rel = None
        self.joystick_ball_y_rel = None

        self.which_joystick_hat = None
        self.joystick_hat = None
        self.joystick_hat_value = None

        self.which_joystick_button_up = None
        self.joystick_button_up = None
        self.joystick_button_state_up = None

        self.which_joystick_button_down = None
        self.joystick_button_down = None
        self.joystick_button_state_down = None

        self.joystick_added = None
        self.joystick_removed = None

        self.joystick_connected = False

    # Takes the joystick input and stores in variables
    def update_sdl2(self, joy_num):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                # self.which_joystick = event.jaxis.which
                # self.joystick_axis[event.jaxis.axis] = event.jaxis.value

                # Should be appending axis data to the corresponding joystick
                self.joystick_axis = []
                for i in range(joy_num):
                    if i == event.jaxis.which:
                        self.joystick_axis.append(event.jaxis.value)

            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.which_joystick_ball = event.jball.which
                self.joystick_ball = event.jball.ball
                self.joystick_ball_y_rel = event.jball.xrel
                self.joystick_ball_y_rel = event.jball.yrel

            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.which_joystick_hat = event.jhat.which
                self.joystick_hat = event.jhat.hat
                self.joystick_hat_value = event.jhat.value

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.which_joystick_button_up = event.jbutton.which
                self.joystick_button_up = event.jbutton.button
                self.joystick_button_state_up = event.jbutton.state

            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.which_joystick_button_down = event.jbutton.which
                self.joystick_button_down = event.jbutton.button
                self.joystick_button_state_down = event.jbutton.state

            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.joystick_number = sdl2.SDL_NumJoysticks()
                self.joystick_added = event.jdevice.which
                for i in range(self.joystick_number):
                    sdl2.SDL_JoystickOpen(i)
                self.joystick_connected = True

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.joystick_number = sdl2.SDL_NumJoysticks()
                self.joystick_removed = event.jdevice.which
                self.joystick_connected = False
