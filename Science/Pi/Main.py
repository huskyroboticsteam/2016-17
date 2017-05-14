from PIL import Image
import sys
import math

Debug = False

# Cuts out the specified part of the image to prepare for sharpness calculations.
def PrepareImageData(ImgData, StartX, StartY, EndX, EndY):
    Output = [[0 for Y in range(StartY, EndY + 1)] for X in range(StartX, EndX + 1)];
    for Y in range(StartY, EndY):
        for X in range(StartX, EndX):
            Output[X - StartX][Y - StartY] = ImgData[X, Y]
    return Output;

# Trying a few algorithms from this paper: http://amnl.mie.utoronto.ca/data/J25.pdf

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

def GetSharpnessVariance(ImgData, Width, Height):
    SumsMean = [0, 0, 0];
    for Y in range(0, Height):
        for X in range(0, Width):
            SumsMean[0] += ImgData[X][Y][0];
            SumsMean[1] += ImgData[X][Y][1];
            SumsMean[2] += ImgData[X][Y][2];

    MeanInt = [0, 0, 0];
    MeanInt[0] = (SumsMean[0] / (Height * Width));
    MeanInt[1] = (SumsMean[1] / (Height * Width));
    MeanInt[2] = (SumsMean[2] / (Height * Width));
    if Debug:
        sys.stdout.write("Mean Colour: " + str(MeanInt[0]) + "," + str(MeanInt[1]) + "," + str(MeanInt[2]));

    SumsVar = [0, 0, 0];
    for Y in range(0, Height):
        for X in range(0, Width):
            SumsVar[0] += (ImgData[X][Y][0] - MeanInt[0]) ** 2;
            SumsVar[1] += (ImgData[X][Y][1] - MeanInt[1]) ** 2;
            SumsVar[2] += (ImgData[X][Y][2] - MeanInt[2]) ** 2;
    SumsVar[0] /= (Width * Height);
    SumsVar[1] /= (Width * Height);
    SumsVar[2] /= (Width * Height);
    return SumsVar[0] + SumsVar[1] + SumsVar[2];

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

        # Shrinks the data to the relevant region, and translates RGB into a single value for easier calculation.
        if Debug:
            sys.stdout.write("Shrinking to [W:" + str(Size[0]) + " H:" + str(Size[1]) + "] by using [X:" + str(Left) + "->" + str(Right) + "],[Y:" + str(Top) + "->" + str(Bottom) + "]\n");
        ImgData = PrepareImageData(ImgDataRaw, Left, Top, Right, Bottom);

        SharpnessBas = GetSharpnessBasic(ImgData, Size[0], Size[1]);
        sys.stdout.write(str(SharpnessBas) + "\n");
        SharpnessVar = GetSharpnessVariance(ImgData, Size[0], Size[1]);
        sys.stdout.write(str(SharpnessVar) + "\n\n");

TestImageSet(30, 35);