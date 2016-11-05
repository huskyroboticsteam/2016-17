__author__ = 'Trevor'
from ArmConverter import ArmConverter
import struct

class JoystickHandler:
    def __init__(self, pygame):
        'Controls the Joystick connection process.'
        self.pygame = pygame
        self.pygame.joystick.init()
        self.numberOfJoysticks = self.pygame.joystick.get_count()
        self.connectedJoystickNumbers = [] # When joystick successfully connected, its ID will be added here
        self.connectedJoysticks = []
        self.numberOfConnectedJoysticks = 0
        self.joysticksEnabled = False
        self.Angle = 0
        self.Speed = 0
        self.Augar = 0
        self.drill_rotate = 0
        self.antidrill_rotate = 0
        self.ServoStatus = 0
        self.ArmConverter = ArmConverter()
        self.armMotorsPacked = False
        self.ScienceSendEnabled = 0
        self.ShoulderRot = 0

        self.AngleEnabled = 1

        for i in range(self.numberOfJoysticks):
            pygame.joystick.Joystick(i).init()

        print(str(self.numberOfJoysticks) + " joysticks connected.")

        if self.numberOfJoysticks > 0:
            JoystickHandler.joysticks_connected = True
        else:
            JoystickHandler.joysticks_connected = False

    def connectJoysticks(self):
        for i in range(self.numberOfJoysticks): # Iterate through all joysticks connected to computer.
            if self.pygame.joystick.Joystick(i).get_button(0): # Check every joystick to see if trigger pulled.
                if i not in self.connectedJoystickNumbers: # Check to make sure joystick wasn't already added
                    self.connectedJoysticks.append(self.pygame.joystick.Joystick(i))
                    self.connectedJoystickNumbers.append(i)
                    self.numberOfConnectedJoysticks += 1
        if self.numberOfConnectedJoysticks == self.numberOfJoysticks:
            self.joysticksEnabled = True

    def scanJoysticks(self):
        if self.numberOfJoysticks > 0:
            angle = (self.joy2value(-self.connectedJoysticks[0].get_axis(0), True))
            speed = (self.joy2value(self.connectedJoysticks[0].get_axis(1), (not self.connectedJoysticks[0].get_button(0))))

            if self.AngleEnabled:
                self.Angle = self.float256(angle, -1, 1)

            self.Speed = self.float256(speed, -1, 1)

        # ARM STUFF:

        if self.numberOfJoysticks > 1:
            sholder_joy = self.arm_joy2value(self.connectedJoysticks[1].get_axis(1))
            sholder_rot_joy = self.arm_joy2value(self.connectedJoysticks[1].get_axis(3))
            self.ShoulderRot = sholder_rot_joy
            elbow_joy = 0
            if self.connectedJoysticks[1].get_button(2): # Might need to flip 2 and 4
                elbow_joy = 1
            elif self.connectedJoysticks[1].get_button(4):
                elbow_joy = -1
            elbow_rot_joy = self.arm_joy2value(self.connectedJoysticks[1].get_axis(0))
            hat_vals = self.connectedJoysticks[1].get_hat(0)
            wrist_joy = hat_vals[1]
            wrist_rot_joy = hat_vals[0]
            claw_pinch = 0
            if self.connectedJoysticks[1].get_button(0): # May need to flip 0 and 1
                claw_pinch = 1
            elif self.connectedJoysticks[1].get_button(1):
                claw_pinch = -1
            arm_speed = 10*(1 - self.joy2value(self.connectedJoysticks[1].get_axis(2), False))
            self.arm_speed = arm_speed

            armMotors = self.ArmConverter.getArmVals(1, sholder_rot_joy, sholder_joy, elbow_joy, elbow_rot_joy, wrist_joy, wrist_rot_joy, claw_pinch, arm_speed)
            self.armMotors = armMotors
            #self.armMotorsPacked = struct.pack("!hhhhhhh",armMotors[0],armMotors[1],armMotors[2],armMotors[3],armMotors[4],armMotors[5],armMotors[6])
            #self.armMotorsPacked = ''.join([chr(armMotors[0]+127),chr(armMotors[1]+127),chr(armMotors[2]+127),chr(armMotors[3]+127),chr(armMotors[4]+127),chr(armMotors[5]+127),chr(armMotors[6]+127)])
            #print armMotors
            #print self.armMotorsPacked

        # SCIENCE STUFF:
        # augar = 128
        # drill_rotate = 0
        # if self.numberOfJoysticks > 1:
        #     if self.connectedJoysticks[1].get_button(0) == True:
        #         augar = (self.joy2value(-self.connectedJoysticks[1].get_axis(1), True))
        #         augar = self.float256(augar, -1, 1)
        #         print("AUGAR: " + str(ord(chr(augar))))
        #     if self.connectedJoysticks[1].get_button(5) == True: #TODO: really button 0?
        #         drill_rotate = 1
        #         print("clockwise!")
        #     elif self.connectedJoysticks[1].get_button(4) == True:
        #         drill_rotate = 2
        #         print("counterclockwise!")
        #     hat = self.connectedJoysticks[1].get_hat(0)
        #     if hat[1] != 0:
        #         self.ServoStatus = 0
        #     elif hat[0] == 1:
        #         self.ServoStatus = 1
        #     elif hat[0] == -1:
        #         self.ServoStatus = 2
        #     # if self.connectedJoysticks[1].get_hat(0) == True:
        #     #     servoStatus = 0
        #     # elif self.connectedJoysticks[1].get_hat(1) == True:
        #     #     servoStatus = 1
        #     # elif self.connectedJoysticks[1].get_hat(2) == True:
        #     #     servoStatus = 2
        #
        # self.Augar = augar
        # self.Drill = drill_rotate

        # for i in range(self.numberOfJoysticks):
        #     angle = (self.joy2value(self.connectedJoysticks[i].get_axis(0), True))
        #     speed = (self.joy2value(self.connectedJoysticks[i].get_axis(1), (not self.connectedJoysticks[i].get_button(0))))
        #
        #     print angle
        #     print speed
        #
        #     augar = 128
        #     drill_rotate = 0
        #     antidrill_rotate = 0
        #     if self.connectedJoysticks[i].get_button(11) == True:
        #         augar = (self.joy2value(-self.connectedJoysticks[i].get_axis(1), True))
        #         augar = self.float256(augar, -1, 1)
        #         print("AUGAR: " + str(ord(chr(augar))))
        #         if self.connectedJoysticks[i].get_button(0) == True:
        #             drill_rotate = 1
        #             print("clockwise is working!")
        #         elif self.connectedJoysticks[i].get_button(1) == True:
        #             antidrill_rotate = 1
        #             print("counterclockwise is working!")

            # this is the arm stuff
            #there are some changes here
            # sholder_joy = self.arm_joy2value(self.connectedJoysticks[i].get_axis(1))
            # sholder_rot_joy = self.arm_joy2value(self.connectedJoysticks[i].get_axis(3))
            # elbow_joy = 0
            # if self.connectedJoysticks[i].get_button(2): # Might need to flip 2 and 4
            #     elbow_joy = 1
            # elif self.connectedJoysticks[i].get_button(4):
            #     elbow_joy = -1
            # elbow_rot_joy = self.arm_joy2value(self.connectedJoysticks[i].get_axis(0))
            # hat_vals = self.connectedJoysticks[i].get_hat(0)
            # wrist_joy = hat_vals[1]
            # wrist_rot_joy = hat_vals[0]
            # claw_pinch = 0
            # if self.connectedJoysticks[i].get_button(0): # May need to flip 0 and 1
            #     claw_pinch = 1
            # elif self.connectedJoysticks[i].get_button(1):
            #     claw_pinch = -1
            # arm_speed = 1 - self.joy2value(self.connectedJoysticks[i].get_axis(2), False)

            # TODO: get vals from invKinimatics
            # TODO: send to rover
            # added mode and default values Trevor, ask Brian to explain

            # ARM STUFF: UNCOMMENT LATER
            #armMotors = self.ArmConverter.getArmVals(0, sholder_rot_joy, sholder_joy, elbow_joy, elbow_rot_joy, wrist_joy, wrist_rot_joy, claw_pinch, arm_speed)
            #print(armMotors)
            # This is the end of the arm stuff

    def sendInput(self,UDPSender, AllStopStatus,PotStopStatus,OShit,EyeSauran):
        if AllStopStatus == True:
            allStopSend = chr(0)
        else:
            allStopSend = chr(1)
        if PotStopStatus == True:
            potStopSend = chr(0)
        else:
            potStopSend = chr(1)
        # send message in form of characters for the potentiometer flag, emergency stop flag, angle, and speedself.armMotorsPacked
        #if self.armMotorsPacked != False:
            #messageUDP = ''.join([potStopSend, allStopSend, chr(self.Angle), chr(self.Speed),chr(self.armMotorsPacked[0]+127),chr(self.armMotorsPacked[1]+127),chr(self.armMotorsPacked[2]+127),chr(self.armMotorsPacked[3]+127),chr(self.armMotorsPacked[4]+127),chr(self.armMotorsPacked[5]+127),chr(self.armMotorsPacked[6]+127)]) #str originally instead of chr ? Also replace zeroes with bytes as above TODO: ADD BUTTON FUNCTIONALITY

        # Camera stuff sending:
        messageUDP = ''.join([potStopSend, allStopSend, chr(self.Angle), chr(self.Speed), chr(OShit), chr(EyeSauran), chr(self.armMotors[0]+1),chr(self.armMotors[1]+1),chr(self.armMotors[2]+1),chr(self.armMotors[3]+1),chr(self.armMotors[4]+1),chr(self.armMotors[5]+1),chr(self.armMotors[6]+1)])

        #messageUDP = ''.join([potStopSend, allStopSend, chr(self.Angle), chr(self.Speed)]) #str originally instead of chr ? Also replace zeroes with bytes as above TODO: ADD BUTTON FUNCTIONALITY
        UDPSender.sendItOff(messageUDP)
        #UDParm.sendItOff(messageUDP)

        #messageScience = ''.join([chr(self.Augar), chr(self.drill_rotate), chr(self.antidrill_rotate)])
        #UDPscienceBALLS.sendItOff(messageScience)

    def sendArmInput(self,UDParmSender):
        if self.armMotorsPacked != False:
            UDParmSender.sendItOff(self.armMotorsPacked)

    def sendScienceInput(self, UDPscienceSender):
        messageSend = ''.join([chr(self.Augar),chr(self.Drill),chr(self.ServoStatus),chr(self.ScienceSendEnabled)])
        UDPscienceSender.sendItOff(messageSend)

    # Processes the joystick values. Doubles if button for extra thrust is down, rounds values below 0.5 to 0
    def joy2value(self, value, half_control=False):
        if half_control:
            value /= 2.0
        if abs(value - 0) < 0.05:
            value = 0
        return value

    #needed for the arm stuff
    def arm_joy2value(self, value):
        if value > .5:
            return 1
        elif value < -.5:
            return -1
        else:
            return 0

    # Maps values to range from 0 to 255
    def float256(self, value, low, high):
        value = 256 * (value - low) / (high - low)
        value = max([value, 0])
        value = min([value, 255])
        return int(value)