
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
//  Serial.begin(9600);
//  Serial.println("boop");
}

void loop() {
//  Serial.println("Quux");
  if (random(0, RAND_PERIOD) == 0) {
//    Serial.println("Foo");
    // forward
    analogWrite(pwm, PWM_VAL);
    digitalWrite(dir, FWD);
    t0 = millis();
    while(digitalRead(sensorPin) == HIGH) {
      delay(10); // wait for the limit switch
    }
//    Serial.println("bar");
    digitalWrite(pwm, 0); // stop the motor
    time_delta = millis() - t0;
    t0 = millis();
    delay(50); // take a short pause to avoid reversing the motor too quickly
    digitalWrite(dir, BWD); // reverse for the same amount of time we went forward
    while(millis() - t0 < time_delta) {
      delay(10);
    }
    analogWrite(pwm, 0);

  }
  delay(1000);

}
