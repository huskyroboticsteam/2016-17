const int POTENTIOMETER_PIN = 3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println(analogRead(POTENTIOMETER_PIN));
}
