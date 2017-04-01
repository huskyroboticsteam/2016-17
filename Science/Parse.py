import Error
from Packet import PacketType

msgQueue = []

# [ LAST TIMESTAMP, CMD_ID1, CMD_VAL, CMD_ID2, CMD_VAL, .... ]
aux_ctrl = []
sys_ctrl = []
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


"""
Parse System Ctrl Packet
"""
def parse_sysctrl(msg):
    pass

"""
Parse Img Request
"""
def parse_imgreq(msg):
    pass


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

