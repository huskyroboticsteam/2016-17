import sys
import struct
import Error
import Util
from Packet import PacketType
from threading import Thread

IMG_REQ_CONST = 6370218008217978682469763330258393040577855L

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
    global msgQueue
    msgQueue += [msg]

"""
Get Message from Queue
"""
def nextMsg():
    global msgQueue
    temp = msgQueue[0]
    del msgQueue[0]
    return temp

"""
Parse message into timestamp and id
"""
def parse(msg):
    global msgQueue
    global reset
    if len(msgQueue) == 0 and reset:
        reset = False  # Set reset back to default value
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
    global aux_ctrl    
    # Set Timestamp
    aux_ctrl[0] = Util.bytesToInt(msg.data, 0, 4)
    # Get Command ID at byte pos 5
    cmd_id = msg.data[5]
    # Get Command Value
    cmd_value = Util.bytesToInt(msg.data, 6, 10)
    aux_ctrl[cmd_id + 1] = cmd_value
    sys.stdout.write(str(aux_ctrl))


"""
Parse System Ctrl Packet
"""
def parse_sysctrl(msg):
    global cam_ctrl
    # Set Timestamp
    sys_ctrl[0] = Util.bytesToInt(msg.data, 0, 4)
    # Find Command ID at byte pos 5
    cmd_id = msg.data[5]
    # Find value as trailing 8 bytes
    cmd_value = Util.bytesToInt(msg.data, 6, 10)
    # Set Controller to specified value at specified location
    sys_ctrl[cmd_id + 1] = cmd_value


"""
Parse Img Request
"""
def parse_imgreq(msg):
    global cam_ctrl
    # Set Timestamp
    cam_ctrl[0] = Util.bytesToInt(msg.data, 0, 4)
    # Get CMD Value
    cmd_value = Util.bytesToInt(msg.data, 5, 28)
    # Throw error if value incorrect
    if cmd_value != IMG_REQ_CONST:
        # Throw invalid request error
        Error.throw(0x0505)
    # Set the camera number
    cmd_camera = msg.data[28]
    cam_ctrl[cmd_camera] = True
    Util.write(str(cam_ctrl))


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
    global cam_ctrl
    global reset
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


"""
Setup Parsing with all zero arrays
"""
def setupParsing():
    global aux_ctrl
    global sys_ctrl
    global cam_ctrl
    aux_ctrl = [0] * 32
    sys_ctrl = [0] * 32
    cam_ctrl = [0] + [False] * 31
    runThread = Thread(target=thread_parsing)
    runThread.start()
