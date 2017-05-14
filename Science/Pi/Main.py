from PIL import Image
import sys
import math
import threading

Debug = False

# Cuts out the specified part of the image to prepare for sharpness calculations.
def PrepareImageData(ImgData, StartX, StartY, EndX, EndY, Out):
    for X in range(StartX, EndX):
        Out[X - StartX] = [-1 for Yl in range(StartY, EndY + 1)]
        for Y in range(StartY, EndY):
            Out[X - StartX][Y - StartY] = ImgData[X, Y]
    return Out;

# Calculates the sharpness of a prepared data set.
def GetSharpnessBasic(ImgData, Width, Height, Out):
    Sum = 0;
    for Y in range(0, Height - 1):
        for X in range(0, Width - 1):
            Sum += ((ImgData[X+1][Y][0] - ImgData[X][Y][0]) ** 2);
            Sum += ((ImgData[X+1][Y][1] - ImgData[X][Y][1]) ** 2);
            Sum += ((ImgData[X+1][Y][2] - ImgData[X][Y][2]) ** 2);
            Sum += ((ImgData[X][Y][0] - ImgData[X][Y+1][0]) ** 2);
            Sum += ((ImgData[X][Y][1] - ImgData[X][Y+1][1]) ** 2);
            Sum += ((ImgData[X][Y][2] - ImgData[X][Y+1][2]) ** 2);
    Out += [Sum];
    return Sum;

# Creates threads of PrepImageData, then passes that data into threads of GetSharpnessBasic. Returns an int representing the shapness of the image.
def CalcImageAsync(ImgData, OffX, OffY, ThreadsX, ThreadsY, SizeX, SizeY):
    Threads = [[0 for Y in range(0, ThreadsY)] for X in range(0, ThreadsX)];
    Outputs = [[[] for Y in range(0, ThreadsY)] for X in range(0, ThreadsX)];
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            StartX = (SizeX / ThreadsX) * X + OffX;
            StartY = (SizeY / ThreadsY) * Y + OffY;
            EndX = ((SizeX / ThreadsX) * (X + 1)) + 1 + OffX;
            EndY = ((SizeY / ThreadsY) * (Y + 1)) + 1 + OffY;
            Outputs[X][Y] = [[] for Xl in range(StartX, EndX + 1)];
            Threads[X][Y] = threading.Thread(target=PrepareImageData, args=(ImgData, StartX, StartY, EndX, EndY, Outputs[X][Y]));

    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            Threads[X][Y].start();
            
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            Threads[X][Y].join();

    ThreadsSharp = [[0 for Y in range(0, ThreadsY)] for X in range(0, ThreadsX)];
    OutputsSharp = [[[] for Y in range(ThreadsY)] for X in range(ThreadsX)];
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            StartX = (SizeX / ThreadsX) * X;
            StartY = (SizeY / ThreadsY) * Y;
            EndX = ((SizeX / ThreadsX) * (X + 1)) + 1;
            EndY = ((SizeY / ThreadsY) * (Y + 1)) + 1;
            ThreadsSharp[X][Y] = threading.Thread(target=GetSharpnessBasic, args=(Outputs[X][Y], EndX - StartX, EndY - StartY, OutputsSharp[X][Y]));
    
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            ThreadsSharp[X][Y].start();
            
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            ThreadsSharp[X][Y].join();

    Value = 0;
    for Y in range(0, ThreadsY):
        for X in range(0, ThreadsX):
            Value += OutputsSharp[X][Y][0];
    return Value;

# Runs tests.
def TestImageSet(Min, Max):
    Images = [];
    for I in range(Min, Max + 1):
        Images += ["Pi/test0" + str(I) + ".jpg"];

    for File in Images:
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

        ThreadOut = CalcImageAsync(ImgDataRaw, Left, Top, 4, 4, Size[0], Size[1]);
        sys.stdout.write(str(ThreadOut) + "\n");

TestImageSet(30, 35);