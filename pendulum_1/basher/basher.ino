
#define FWD HIGH
#define BWD LOW
#define PWM_VAL 255
const int sensorPin = 2;
const int pwm =  3;
const int dir = 11;
const int RAND_PERIOD = 5; // 10 seconds
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;

void setup() {
  pinMode(pwm, OUTPUT);
  analogWrite(pwm, 0);
  pinMode(dir, OUTPUT);
  pinMode(sensorPin, INPUT);
  randomSeed(analogRead(0));
}

void loop() {
  if (random(0, RAND_PERIOD) == 0) {
    // forward
    analogWrite(pwm, PWM_VAL);
    digitalWrite(dir, FWD);
    t0 = millis();
    while(digitalRead(sensorPin) == HIGH) {
      delay(1); // wait for the limit switch
    }
    time_delta = millis() - t0;
    t0 = millis();
    digitalWrite(dir, BWD); // reverse for the same amount of time we went forward
    while(millis() - t0 < time_delta) {
      delay(10);
    }
    analogWrite(pwm, 0);
  }
  delay(1000);

}
