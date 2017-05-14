from PIL import Image
import sys
import math
import time

Debug = False

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

# Calculates sharpness for a list of images.
def TestImageSet(Min, Max):
    Images = [];
    for I in range(Min, Max + 1):
        Images += ["test0" + str(I) + ".jpg"];

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

        # Shrinks the data to the relevant region, and translates RGB into a single value for easier calculation.
        if Debug:
            sys.stdout.write("Shrinking to [W:" + str(Size[0]) + " H:" + str(Size[1]) + "] by using [X:" + str(Left) + "->" + str(Right) + "],[Y:" + str(Top) + "->" + str(Bottom) + "]\n");
        ImgData = PrepareImageData(ImgDataRaw, Left, Top, Right, Bottom);

        SharpnessBas = GetSharpnessBasic(ImgData, Size[0], Size[1]);
        sys.stdout.write(str(SharpnessBas) + "\n");

millisS = int(round(time.time() * 1000))
TestImageSet(30, 35);
millisE = int(round(time.time() * 1000))
sys.stdout.write("Took " + str(millisE - millisS) + "ms.\n")