from PIL import Image
import socket
import sys
import math
import time
import os
import struct
import RPi.GPIO as GPIO
from subprocess import call
from binascii import unhexlify
import signal
import traceback

Debug = False
ExpectedRange = (15, 345);

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
    GPIO.cleanup();
    sys.exit(0);

# Simply takes a picture.
def TakePicture(File):
    call(["fswebcam", "-r", "1600x1200", File]);
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
        Sock.connect(("192.168.0.90", 5000));
        Sock.send(Timestamp + ID + Command + Value);
        Sock.close()
    except:
        sys.stdout.write("Something went wrong when sending packet.\n");
        sys.stdout.write(traceback.format_exc());

# Executes the AF routine.
def DoAutofocus():
    File = GetFilename(True, False);
    TakePicture(File);
    if Debug:
        sys.stdout.write("Picture taken, calculating sharpness...\n");
    Sharpness = TestImage(File);
    if Debug:
        sys.stdout.write("Sharpness: " + str(Sharpness) + "\n");
    while LimitMoveAndContinue(Cycle(Sharpness)):
        File = GetFilename(True, False);
        TakePicture(File);
        if Debug:
            sys.stdout.write("Picture taken, calculating sharpness...\n");
        Sharpness = TestImage(File);
        if Debug:
            sys.stdout.write("Sharpness: " + str(Sharpness) + "\n");
    GetFilename(True, True); # Moves to next folder.
signal.signal(signal.SIGINT, UserExit)

GPIO.setmode(GPIO.BOARD);
InputPin = 16;
GPIO.setup(InputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN);
TakePic = False;
DoAF = False;
ServoPos = ExpectedRange[0] * (1);

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
FocusIsNear = False;
MovementQty = 50.000;

# If we're about to exit focus bounds, turn around. Check if movement needs to happen, and do it. Returns False if we're done taking this picture.
def LimitMoveAndContinue(Movement):
    global PicFoci;
    global FocusIsNear;
    global MovementQty;
    global ServoPos;
    global ExpectedRange;
    if abs(Movement) > 0.25:
        if (ServoPos + Movement) < ExpectedRange[0] or (ServoPos + Movement) > ExpectedRange[1]:
            Movement *= -1;
            MovementQty *= -1; # Keep it going in the new direction.
        ServoPos += Movement;
        SendServo(ServoPos % 360);
        if Debug:
            sys.stdout.write("Packet sent for servo pos " + str(ServoPos % 360) + ".\n");
        time.sleep(1);
        return True;
    else:
        PicFoci = [];
        FocusIsNear = False;
        MovementQty = 50.000;
        ServoPos = 0;
        time.sleep(2);
        return False;

def Cycle(CurrFocus):
    global PicFoci;
    global FocusIsNear;
    global MovementQty;
    PicFoci += [CurrFocus];
    Avg = AvgList(PicFoci);
    if len(PicFoci) >= 20:
        # We've taken 20 pictures, so we're probably OK to stop.
        # Either we are close enough, or we ran into issues and won't find a good focus point.
        return 0.000;
    if PicFoci > (Avg * 1.2):
        # We are close, slow down, and check direction.
        if PicFoci[len(PicFoci) - 2] > CurrFocus:
            # We were better, go back slowly.
            MovementQty *= -0.75;
        else:
            # We are still improving. Slow down to minimize overshoot.
            MovementQty *= 0.75;
        FocusIsNear = True;
    elif FocusIsNear:
        # Focus was near, no longer. We need to go back.
        MovementQty *= -0.75;
        return MovementQty;
    else:
        # Focus was not near, and still is not. Keep going.
        return MovementQty;
    return 50.000;

def AvgList(List):
    Sum = 0;
    for I in List:
        Sum += I;
    return (Sum) / len(List);

call(["fuser", "/dev/video0", "-k"]);
GetFilename(True, True);
GPIO.add_event_detect(InputPin, GPIO.RISING, callback=CamTrigger);

if len(sys.argv) > 0:
    sys.stdout.write("Arguments given: " + str(sys.argv) + "\n");
    for Argument in sys.argv:
        if(Argument == "d"):
            Debug = True;
            sys.stdout.write("Debug mode enabled.\n");
        if(Argument == "a"):
            TakePic = True;
            DoAF = True;
            break;
        if(Argument == "p"):
            TakePic = True;
            DoAF = False;
            break;  

while True:
    if TakePic:
        if DoAF:
            DoAutofocus();
            TakePic = False;
        else:
            TakePicture(GetFilename(True, True));
            TakePic = False;
    time.sleep(0.050);
GPIO.cleanup();