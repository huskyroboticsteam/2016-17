//These variables need to stay out of the fuction because if they are in they get reset and we don't want that
unsigned long Time;
int EncoderCount = 0;
int lastEncoder;

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
 double Motor2_AngVel = CalcAngVel(2);
 if (Motor2_AngVel != 1)
 {
 Serial.print("AngVel: ");
 Serial.println(Motor2_AngVel);
 Serial.println(" Rotations/s");
 }
}

double CalcAngVel(int port)
{
  // Motor is 48:1 gearing, with an 8 pole magnet, meaning 1 roation is 384 ticks
  // Some local variables for the function
  int SampleSize = 100; // in ms
  int Encoder; 
  double AngVel = 0;

  //Reads the encoder input as either a 1 or a 0 from the specified port
  Encoder = (digitalRead(port));

  //Checks to see if the encoder has moved. If yes, incriments the count up by one
  if (Encoder != lastEncoder)
  {EncoderCount ++;}
  //Sets current value as the last value for future comparison
  lastEncoder = Encoder;

  //Checks to see if the sample taking time is up. If yes then it calculates angular velocity
  if (millis() - Time > SampleSize)
  {
    AngVel = (double(EncoderCount)/384)/(SampleSize/1000.0);
    Time = millis();
    // Resets encoder count so we don't double count in the future
    EncoderCount = 0;
    Serial.println(AngVel);
    return AngVel;
  }
  return -1;
}

