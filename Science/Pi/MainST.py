from PIL import Image
import socket
import sys
import math
import time
import os
import struct
# import RPi.GPIO as GPIO #<platform>
from subprocess import call
from binascii import unhexlify
import signal
import traceback

Debug = False
ExpectedRange = (90, 225);

def GetFilename(BoolAddToFile, BoolAddFolder):
    FolderNm = "imgs";
    FileNm = "img";
    try:
        Lines = open("NODELETE_Current.txt").read().splitlines();
        if Debug:
            sys.stdout.write("Folder/File: " + str(Lines[0]) + "\n");
        if BoolAddFolder:
            Lines[0] = str(int(Lines[0]) + 1);
            Lines[1] = "0";
        else:
            Lines[0] = str(int(Lines[0]));
            Lines[1] = str(int(Lines[1]) + 1);
        FolderNm += Lines[0];
        FileNm += Lines[1] + ".jpg";
        if BoolAddToFile:
            open("NODELETE_Current.txt",'w').write('\n'.join(Lines));
    except:
        sys.stdout.write("Record file is missing!\n");
        sys.stdout.write(traceback.format_exc());
        return "ERROR_OVERZEALOUS_DELETION.jpg";
    if not os.path.exists(FolderNm):
        os.makedirs(FolderNm);
    return FolderNm + "/" + FileNm;

# Cuts out the specified part of the image to prepare for sharpness calculations.
def PrepareImageData(ImgData, StartX, StartY, EndX, EndY):
    Output = [[0 for Y in range(StartY, EndY + 1)] for X in range(StartX, EndX + 1)];
    for Y in range(StartY, EndY):
        for X in range(StartX, EndX):
            Output[X - StartX][Y - StartY] = ImgData[X, Y]
    return Output;

# Calculates the sharpness of a prepared data set.
def GetSharpnessBasic(ImgData, Width, Height):
    Sum = 0;
    for Y in range(0, Height - 1):
        for X in range(0, Width - 1):
            Sum += ((ImgData[X+1][Y][0] - ImgData[X][Y][0]) ** 2);
            Sum += ((ImgData[X+1][Y][1] - ImgData[X][Y][1]) ** 2);
            Sum += ((ImgData[X+1][Y][2] - ImgData[X][Y][2]) ** 2);
            Sum += ((ImgData[X][Y][0] - ImgData[X][Y+1][0]) ** 2);
            Sum += ((ImgData[X][Y][1] - ImgData[X][Y+1][1]) ** 2);
            Sum += ((ImgData[X][Y][2] - ImgData[X][Y+1][2]) ** 2);
    return Sum;

def TestImage(File):
    if Debug:
            sys.stdout.write("=== Image: " + File + " ===\n");
    # Opens the image and gets basic parameters.
    ImgObj = Image.open(File);
    ImgDataRaw = ImgObj.load();
    SizeRaw = ImgObj.size;
    if Debug:
        sys.stdout.write("Raw dimensions: [W:" + str(SizeRaw[0]) + " H:" + str(SizeRaw[1]) + "]\n");

    # The region that will be checked for sharpness.
    Left = (SizeRaw[0] * 1/3);
    Right = (SizeRaw[0] * 2/3);
    Top = (SizeRaw[1] * 1/3);
    Bottom = (SizeRaw[1] * 2/3);
    Size = (Right - Left), (Bottom - Top);

    # Shrinks the data to the relevant region, and translates RGB into a single value for easier calculation.
    if Debug:
        sys.stdout.write("Shrinking to [W:" + str(Size[0]) + " H:" + str(Size[1]) + "] by using [X:" + str(Left) + "->" + str(Right) + "],[Y:" + str(Top) + "->" + str(Bottom) + "]\n");
    ImgData = PrepareImageData(ImgDataRaw, Left, Top, Right, Bottom);
    SharpnessBas = GetSharpnessBasic(ImgData, Size[0], Size[1]);
    if Debug:
        sys.stdout.write("Calculated sharpness: " + str(SharpnessBas) + "\n");
    return SharpnessBas;

def FakeImage():
    FakeValues = [51116, 47931, 48354, 48792, 50671, 47892, 40102, 40863, 43109, 46631, 39613, 42914, 39940, 43754, 44793, 44170, 46007, 51511, 43228, 39744, 40873, 45067, 47988, 42363, 42916, 43172, 47291, 45896, 46850, 45183, 45729, 41245, 50210, 52495, 47536, 45695, 48008, 43642, 44849, 41600, 44970, 44671, 41289, 39644, 45333, 42699, 46530, 49093, 48331, 44409, 48998, 48565, 39850, 47529, 46387, 49292, 40966, 40997, 50828, 40451, 50618, 50496, 39269, 46406, 41950, 41289, 45614, 51213, 52066, 52924, 47108, 52148, 47210, 46298, 53342, 51481, 40690, 51413, 41615, 44942, 47313, 49308, 42190, 46430, 49575, 50559, 40843, 51275, 43865, 44705, 53003, 42781, 50581, 42241, 50723, 45741, 53149, 43518, 52466, 51123, 52266, 50872, 45569, 52801, 50861, 40116, 46406, 53177, 40452, 53222, 47152, 52292, 46346, 47341, 44145, 48080, 44444, 42155, 42890, 55138, 55135, 41764, 48764, 47284, 47679, 45514, 43888, 42137, 48348, 50406, 54700, 51694, 45192, 42369, 41455, 52459, 50785, 49567, 49214, 49280, 50292, 54029, 49299, 50839, 51361, 48398, 48862, 49348, 44907, 56284, 55173, 43894, 53196, 43287, 50944, 48137, 53419, 50207, 47996, 53508, 46178, 49269, 54191, 47464, 43327, 42730, 48598, 50851, 54734, 53175, 41846, 54224, 49965, 53448, 43054, 48924, 46580, 42703, 53252, 47288, 47008, 49109, 53949, 56153, 56164, 52665, 56629, 51547, 45214, 48041, 47283, 44178, 45030, 48929, 50515, 54572, 58549, 49198, 47593, 58325, 52783, 44438, 51960, 51227, 55239, 49901, 48800, 59262, 58962, 59157, 52768, 53617, 52958, 51804, 79112, 72806, 106617, 121564, 211783, 510948, 878183, 1936569, 1097830, 485215, 92455, 71501, 62339, 72318, 67332, 54635, 53578, 46378, 53904, 50400, 44736, 57467, 46124, 44454, 48401, 52328, 50535, 47863, 50880, 54408, 46953, 51617, 43791, 52957, 54115, 47796, 46324, 44832, 56296, 42503, 42163, 51149, 54866, 50148, 46947, 45386, 49164, 47030, 45707, 43302, 47682, 54375, 48084, 46334, 52906, 46886, 54390, 46496, 48711, 53289, 52855, 44622, 43045, 47239, 52563, 42826, 42981, 51978, 40903, 51820, 39538, 42653, 51288, 49755, 41813, 49812, 49453, 46341, 49457, 51687, 47153, 42381, 43632, 45133, 48278, 52429, 44464, 49650, 51289, 47762, 47152, 46297, 41378, 40439, 49653, 39638, 41240, 40631, 44372, 47440, 41448, 47914, 45467, 46654, 51111, 44831, 47156, 42576, 38752, 40816, 47715, 44883, 41097, 45126, 50917, 46968, 44512, 47370, 50415, 43412, 45777, 47388, 48698, 51617, 39196, 40173, 48008, 42791, 45687, 39866, 49690, 44428, 49794, 49345, 49416, 45290, 49968, 47767, 44017, 49639, 43142, 44279, 47092, 49534, 46814, 49078, 42608];
    if Debug:
        sys.stdout.write("Faking image sharpness, servo at " + str(ServoPos) + ", so returning " + str(FakeValues[int(ServoPos % 360)]) + ".\n");
    return FakeValues[int(ServoPos % 360)];

# Calculates sharpness for a list of images.
def TestImageSet(Min, Max):
    Images = [];
    for I in range(Min, Max + 1):
        Images += ["test0" + str(I) + ".jpg"];

    for File in Images:
        sys.stdout.write(str(TestImage(File)));

# Taken from Util.py by @baldstrom.
def long_to_bytes(val, endianness='big'):
    if val < 0:
        return struct.pack('<l', val)
    if val == 0:
        return '\x00'
    width = val.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % val)
    if endianness == 'little':
        s = s[::-1]
    return s

# Taken from Util.py by @baldstrom.
def long_to_byte_length(val, byte_length, endianness='big'):
    valBA = bytearray(long_to_bytes(val))
    if len(valBA) > byte_length:
        valBA = valBA[:byte_length]
    elif len(valBA) < byte_length:
        valBA = b'\x00'*(byte_length-len(valBA)) + valBA
    return valBA

def UserExit(signal, frame):
    sys.stdout.write("Ctrl+C detected, exiting...\n");
    #GPIO.cleanup(); #<platform>
    sys.exit(0);

# Simply takes a picture.
def TakePicture(File):
    call(["fswebcam", "-r", "1600x1200", File]); #<platform>
    pass;

# Sends a "move servo" packet to the BeagleBone. Used for AF.
def SendServo(NewValue):
    Timestamp = long_to_byte_length(int(time.time()), 4);
    ID = long_to_byte_length(0x81, 1);
    Command = long_to_byte_length(0x02, 1);
    Value = long_to_byte_length(int(NewValue), 4);
    try:
        Sock = socket.socket();
        #TimeoutVal = struct.pack('ll', 8, 8000000);
        #Sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, TimeoutVal)
        #Sock.connect(("192.168.0.90", 5000)); #<platform>
        #Sock.send(Timestamp + ID + Command + Value); #<platform>
        #Sock.close() #<platform>
    except:
        sys.stdout.write("Something went wrong when sending packet.\n");
        sys.stdout.write(traceback.format_exc());

# Executes the AF routine.
def DoAutofocus():
    """File = GetFilename(True, False);
    TakePicture(File);
    if Debug:
        sys.stdout.write("Picture taken, calculating sharpness...\n");
    Sharpness = TestImage(File);
    if Debug:
        sys.stdout.write("Sharpness: " + str(Sharpness) + "\n");"""
    Sharpness = FakeImage();
    LimitMoveAndContinue(Cycle(Sharpness));
    while LimitMoveAndContinue(Cycle(Sharpness)):
        Sharpness = FakeImage();
        """File = GetFilename(True, False);
        TakePicture(File);
        if Debug:
            sys.stdout.write("Picture taken, calculating sharpness...\n");
        Sharpness = TestImage(File);
        if Debug:
            sys.stdout.write("Sharpness: " + str(Sharpness) + "\n");"""
    #GetFilename(True, True); # Moves to next folder.
signal.signal(signal.SIGINT, UserExit)

#GPIO.setmode(GPIO.BOARD); #<platform>
InputPin = 16;
#GPIO.setup(InputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN); #<platform>
TakePic = False;
DoAF = False;
ServoPos = ExpectedRange[0];

def CamTrigger(channel):
    global DoAF;
    global TakePic;
    time.sleep(0.150);
    if(GPIO.input(InputPin)):
        DoAF = False;
        TakePic = True;
    else:
        DoAF = True;
        TakePic = True;

PicFoci = [];
ServoPositions = [];
FocusIsNear = False;
FocusWasVeryGood = False;
MovementQty = 25.000;

# If we're about to exit focus bounds, turn around. Check if movement needs to happen, and do it. Returns False if we're done taking this picture.
def LimitMoveAndContinue(Movement):
    global PicFoci;
    global ServoPositions;
    global FocusIsNear;
    global MovementQty;
    global ServoPos;
    global ExpectedRange;
    global FocusWasVeryGood;
    if abs(Movement) > 0.75:
        if (ServoPos + Movement) < ExpectedRange[0] or (ServoPos + Movement) > ExpectedRange[1]:
            Movement *= -0.5;
            MovementQty *= -1; # Keep it going in the new direction.
        ServoPos += Movement;
        SendServo(ServoPos % 360);
        if Debug:
            sys.stdout.write("Packet sent for servo pos " + str(ServoPos % 360) + ".\n");
        time.sleep(1);
        return True;
    else:
        if Debug:
            sys.stdout.write("Tested servo positions: " + str(ServoPositions) + "\n");
        PicFoci = [];
        ServoPositions = [];
        FocusIsNear = False;
        FocusWasVeryGood = False;
        MovementQty = 25.000;
        ServoPos = 0;
        time.sleep(2);
        return False;

def Cycle(CurrFocus):
    global PicFoci;
    global ServoPositions;
    global FocusIsNear;
    global FocusWasVeryGood;
    global MovementQty;
    global ServoPos;
    PicFoci += [CurrFocus];
    ServoPos = int(ServoPos);
    ServoPositions += [ServoPos];
    Avg = AvgList(PicFoci);
    if len(PicFoci) >= 40:
        # We've taken 40 pictures, so we're probably OK to stop.
        # Either we are close enough, or we ran into issues and won't find a good focus point.
        if Debug:
            sys.stdout.write("[C] We've taken 40 pictures, giving up.\n");
        return 0.000;
    if CurrFocus > (Avg * 1.2):
        # We are close, slow down, and check direction.
        if PicFoci[len(PicFoci) - 2] > CurrFocus * 1.05:
            if Debug:
                sys.stdout.write("[C] Close, but we were better. Moving back slowly.\n");
            MovementQty *= -0.6;
        else:
            if Debug:
                sys.stdout.write("[C] Close, we are still improving. Slowing down to minimize overshoot.\n");
            if FocusIsNear: # We were already close, slow down significantly.
                if CurrFocus > (Avg * 5):
                    if Debug:
                        sys.stdout.write("[C] Focus is very good. Slowing down quite a bit.\n");
                    FocusWasVeryGood = True;
                    MovementQty *= 0.5;
                if abs(MovementQty) < 3:
                    if Debug:
                        sys.stdout.write("[C] We're already moving slow. Not stopping yet.\n");
                    # We're already quite slow, don't slow as much.
                    MovementQty *= (1 / MovementQty);
                else:
                    if FocusWasVeryGood:
                        MovementQty *= -0.5;
                    else:
                        MovementQty *= 0.5;
            else: # We just got near. Slow down a bit less.
                MovementQty *= 0.6;
        FocusIsNear = True;
    elif FocusIsNear:
        if Debug:
            sys.stdout.write("[C] Focus was near, no longer. We need to go back.\n");
        MovementQty *= -0.95;
        FocusIsNear = False;
        return MovementQty;
    else:
        if Debug:
            sys.stdout.write("[C] Focus was not near, and still is not. Keep going.\n");
        return MovementQty;
    return MovementQty;

def AvgList(List):
    Sum = 0;
    for I in List:
        Sum += I;
    return (Sum) / len(List);

#call(["fuser", "/dev/video0", "-k"]); #<platform>
GetFilename(True, True);
#GPIO.add_event_detect(InputPin, GPIO.RISING, callback=CamTrigger); #<platform>

if len(sys.argv) > 0:
    sys.stdout.write("Arguments given: " + str(sys.argv) + "\n");
    for Argument in sys.argv:
        if(Argument == "d"):
            Debug = True;
            sys.stdout.write("Debug mode enabled.\n");
        if(Argument == "a"):
            TakePic = True;
            DoAF = True;
        if(Argument == "p"):
            TakePic = True;
            DoAF = False;

while True:
    if TakePic:
        if DoAF:
            DoAutofocus();
            TakePic = False;
        else:
            TakePicture(GetFilename(True, True));
            TakePic = False;
    time.sleep(0.050);
#GPIO.cleanup(); #<platform>