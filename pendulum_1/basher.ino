
#define FWD HIGH
#define BWD LOW

const int sensorPin = 2;
const int relay1 =  12;
const int relay2 = 11;
const int RAND_PERIOD = 10; // 10 seconds
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;

void setup() {
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(sensorPin, INPUT);
  randomSeed(analogRead(0));
}

void loop() {
  if (random(0, RAND_PERIOD) == RAND_PERIOD) {
    // forward
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
    t0 = millis();
    while(digitaRead(sensorPin) == LOW) {
      delay(10); // wait for the limit switch
    }
    digitalWrite(relay1, LOW); // stop the motor
    time_delta = millis() - t0;
    t0 = millis();
    delay(50); // take a short pause to avoid reversing the motor too quickly
    digitalWrite(relay2, HIGH); // reverse for the same amount of time we went forward
    while(millis() - t0 < time_delta) {
      delay(10);
    }
    digitalWrite(relay2, LOW);

  }
  delay(1000);

}