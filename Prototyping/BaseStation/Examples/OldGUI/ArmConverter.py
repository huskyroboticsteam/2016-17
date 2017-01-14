__author__ = 'Trevor'

class ArmConverter:
    def __init__(self):
        self.sholderRot = 0
        self.sholder = 0
        self.elbow = 0
        self.elbowRot = 0
        self.wrist = 0
        self.wristRot = 0
        self.hand = 0
        self.humLen = 20
        self.forarmLen = 15
        self.handLen = 5
    #
    # def up_down(self, dx):
    #     global sholder, wrist
    #     sholder += dx
    #     wrist -= dx
    #     if not (self.inRange(sholder) and self.inRange(wrist)):
    #         sholder -= dx
    #         wrist += dx
    #
    # def left_right(self, dx):
    #     global sholderRot
    #     sholderRot += dx
    #     if not self.inRange(sholderRot):
    #         sholderRot -= dx
    #
    # def forward_back(self, dx):
    #     global sholder, elbow
    #     sholder += dx
    #     elbow += dx
    #     if not (self.inRange(sholder) and self.inRange(elbow)):
    #         sholder -= dx
    #         elbow -= dx
    #
    # def twistHand(self, dx):
    #     global wristRot
    #     wristRot += dx
    #     if not self.inRange(wristRot):
    #         wristRot -= dx
    #
    # def twistForarm(self, dx):
    #     global elbowRot
    #     elbowRot += dx
    #     if not self.inRange(elbowRot):
    #         elbowRot -= dx
    #
    # def hand_open_close(self, dx):
    #     global hand
    #     hand += dx
    #     if not self.inRange(hand):
    #         hand -= dx
    #
    #
    # def InverseKin(self):
    #     return False

    def ZeroPosition(self):
        #global sholderRot, sholder, elbow, elbowRot, wrist, wristRot, hand
        self.sholderRot = 0
        self.sholder = 0
        self.elbow = 0
        self.elbowRot = 0
        self.wrist = 0
        self.wristRot = 0
        self.wrist = 0
        self.hand = 0

    def inRange(self, x):
        return x < 180 and x > -180

    # takes in joystick imput values and coverts to motor vals
    # returns a 7-length array of vals
    def getArmVals(self, mode, arm_left_right, arm_forward_back, arm_up_down, extra_elbow_rot, extra_wrist, wrist_twist, claw_open_close, arm_speed):
        #global sholderRot, sholder, elbow, elbowRot, wrist, wristRot, hand
        if mode == 0:
            temp = [arm_left_right, arm_forward_back, arm_up_down, extra_elbow_rot, extra_wrist, wrist_twist, claw_open_close]
            vals = [int(x * arm_speed * 5) for x in temp]
            return vals
            # self.sholderRot = self.sholderRot + vals[0]
            # self.sholder = self.sholder + vals[1]
            # self.elbow = self.elbow + vals[2]
            # self.elbowRot = self.elbowRot + vals[3]
            # self.wrist = self.wrist + vals[4]
            # self.wristRot = self.wristRot + vals[5]
            # self.hand = self.hand + vals[6]
        # elif mode == 1:
        #     self.forward_back(arm_forward_back * 5)
        #     self.up_down(arm_up_down  * 5)
        #     self.left_right(arm_left_right * 5)
        #     self.twistHand(wrist_twist * 5)
        #     self.hand_open_close(claw_open_close * 5)
        # elif mode == 2:
        #     self.InverseKin()
        else:
            return [arm_left_right, arm_forward_back, arm_up_down, extra_elbow_rot, extra_wrist, wrist_twist, claw_open_close]
        #return [self.sholderRot, self.sholder, self.elbow, self.elbowRot, self.wrist, self.wristRot, self.hand]