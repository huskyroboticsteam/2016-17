from PIL import Image
import sys
import math

"""
    Cuts out the specified part of the image, and translates RGB into a single value to prepare for sharpness calculations.
"""
def PrepareImageData(ImgData, StartX, StartY, EndX, EndY):
    Output = [[0 for Y in range(StartY, EndY + 1)] for X in range(StartX, EndX + 1)];
    for Y in range(StartY, EndY):
        for X in range(StartX, EndX):
            #sys.stdout.write("At " + str(X) + "->" + str(X - StartX) + ", " + str(Y) + "->" + str(Y - StartY) + "\n")
            Pixel = ImgData[X, Y];
            Output[X - StartX][Y - StartY] = (Pixel[0]) + ((Pixel[1]) << 8) + ((Pixel[2]) << 16);
    return Output;

def GetSharpness(ImgData, Width, Height):
    Sum = 0;
    for Y in range(0, Height - 1):
        for X in range(0, Width - 1):
            #if (X > (Width - 10)) or (Y > (Height - 10)):
                #sys.stdout.write(str(X) + " " + str(Y) + "\n");

            #sys.stdout.write(str(ImgData));
            Sum += (ImgData[X+1][Y] - ImgData[X][Y]) ** 2;
            Sum += (ImgData[X+1][Y] - ImgData[X][Y]) ** 2;
    return Sum;

Images = ["Pi/test001.jpg", "Pi/test002.jpg", "Pi/test003.jpg", "Pi/test004.jpg", "Pi/test005.jpg", "Pi/test006.jpg", "Pi/test007.jpg", "Pi/test008.jpg", "Pi/test009.jpg", "Pi/test010.jpg", "Pi/test011.jpg", "Pi/test012.jpg"];

for File in Images:
    sys.stdout.write("=== Image: " + File + " ===\n");
    ImgObj = Image.open(File);
    ImgDataRaw = ImgObj.load();
    SizeRaw = ImgObj.size;
    sys.stdout.write("Raw dimensions: [W:" + str(SizeRaw[0]) + " H:" + str(SizeRaw[1]) + "]\n");

    Left = (SizeRaw[0] * 1/3);
    Right = (SizeRaw[0] * 2/3);
    Top = (SizeRaw[1] * 1/3);
    Bottom = (SizeRaw[1] * 2/3);
    Size = (Right - Left), (Bottom - Top);

    sys.stdout.write("Shrinking to [W:" + str(Size[0]) + " H:" + str(Size[1]) + "] by using [X:" + str(Left) + "->" + str(Right) + "],[Y:" + str(Top) + "->" + str(Bottom) + "]\n");
    ImgData = PrepareImageData(ImgDataRaw, Left, Top, Right, Bottom);

    Sharpness = GetSharpness(ImgData, Size[0], Size[1]);
    sys.stdout.write("F:" + str(Sharpness) + "\n\n");
