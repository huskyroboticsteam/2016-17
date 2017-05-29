from PIL import Image
import socket
import sys
import math
import time
import os
import struct
import RPi.GPIO as GPIO #<platform>
from subprocess import call
from binascii import unhexlify
import signal
import traceback

Debug = False
ExpectedRange = (0, 360);

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
    GPIO.cleanup(); #<platform>
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
        Sock.connect(("192.168.0.90", 5000)); #<platform>
        Sock.send(Timestamp + ID + Command + Value); #<platform>
        Sock.close() #<platform>
    except:
        sys.stdout.write("Something went wrong when sending packet.\n");
        sys.stdout.write(traceback.format_exc());

# Executes the AF routine.
def DoAutofocus():
    global PicFoci;
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
    # Finds the best picture and labels it as so for the operator.
    BestPicture = 0;
    for Pic in range(0, len(PicFoci)):
        if(PicFoci[Pic] > PicFoci[BestPicture]):
            BestPicture = Pic;
    sys.stdout.write("-> Best picture was " + str(BestPicture + 1) + ".\n");
    CurrFolder = GetFilename(False, False).split('/')[0];
    BestPicFile = CurrFolder + "/img" + str(BestPicture) + ".jpg";
    call(["cp", BestPicFile, CurrFolder + "/BEST_PICTURE.jpg"]); #<platform>
    PicFoci = [];
    ServoPositions = [];
    FocusIsNear = False;
    FocusWasVeryGood = False;
    MovementQty = 25.000;
    ServoPos = 0;
    time.sleep(1);
    GetFilename(True, True); # Moves to next folder.
signal.signal(signal.SIGINT, UserExit)

GPIO.setmode(GPIO.BOARD); #<platform>
InputPin = 16;
GPIO.setup(InputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN); #<platform>
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

call(["fuser", "/dev/video0", "-k"]); #<platform>
GetFilename(True, True);
GPIO.add_event_detect(InputPin, GPIO.RISING, callback=CamTrigger); #<platform>

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
GPIO.cleanup(); #<platform>