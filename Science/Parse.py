import Error
from Packet import PacketType

msgQueue = []

# [ LAST TIMESTAMP, CMD_VAL_ID1, CMD_VAL_ID2, ... ]
aux_ctrl = []
sys_ctrl = []

"""
*** WHEN PICTURE IS CAPTURED, THE RESPECTIVE
    CAMERA ID, SHOULD BE SET TO 'False' IN
    THIS HANDLER ARRAY.
"""
# [ LAST TIMESTAMP, CAM_NUM0_BOOL, CAM_NUM1_BOOL, ... ]
cam_ctrl = []

reset = False

"""
Queue a message to the handler
"""
def queueMessage(msg):
    msgQueue[len(msgQueue) - 1] = msg

"""
Get Message from Queue
"""
def nextMsg():
    temp = msgQueue[0]
    del msgQueue[0]
    return temp

"""
Parse message into timestamp and id
"""
def parse(msg):
    global reset
    if len(msgQueue) == 0 and reset:
        reset = False
    if msg.ID == PacketType.AuxControl:
        parse_aux(msg)
    elif msg.ID == PacketType.SysControl:
        parse_sysctrl(msg)
    elif msg.ID == PacketType.ImageRequest:
        parse_imgreq(msg)
    else:
        # Throw Failed to Parse incoming Packet
        Error.throw(0x0504)

"""
Parse Auxilliary Ctrl Packet
"""
def parse_aux(msg):
    aux_ctrl[0] = int(msg.data[0:33])
    cmd_id = int(msg.data[40:48])
    cmd_value = int(msg.data[48:80])
    aux_ctrl[cmd_id + 1] = cmd_value


"""
Parse System Ctrl Packet
"""
def parse_sysctrl(msg):
    cam_ctrl[0] = int(msg.data[0:33])
    cmd_id = int(msg.data[40:48])
    cmd_value = int(msg.data[48:80])
    cam_ctrl[cmd_id + 1] = cmd_value


"""
Parse Img Request
"""
def parse_imgreq(msg):
    cam_ctrl[0] = int(msg.data[0:33])
    cmd_id = int(msg.data[40:48])
    cmd_value = int(msg.data[48:192])
    if cmd_value != "I can haz picture?":
        # Throw invalid request error
        Error.throw(0x0505)
    cmd_camera = int(msg.data[192:200])
    cam_ctrl[cmd_camera] = True


"""
Parsing Handler
"""
def parse_all():
    while len(msgQueue) > 0:
        parse(nextMsg())


"""
Threading method, call to setup thread
"""
def thread_parsing():
    while True:
        if reset:
            msgQueue = []
        parse_all()


"""
Call every camera capture
"""
def resetCam():
    for i in range(1, len(cam_ctrl)):
        cam_ctrl[i] = False



def setupParsing():
    aux_ctrl = [0] * 32
    sys_ctrl = [0] * 32
    cam_ctrl = [0] + [False] * 31
