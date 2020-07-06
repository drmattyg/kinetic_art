
#define FWD HIGH
#define BWD LOW
#define PWM_VAL 85
const int sensorFwd = 8;
const int sensorRev = 6;
const int pwm =  3;
const int dir = 11;
const int led = 13;
const int RAND_PERIOD = 5; // 10 seconds
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;

void setup() {
  pinMode(pwm, OUTPUT);
  analogWrite(pwm, 0);
  pinMode(dir, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(sensorFwd, INPUT);
  pinMode(sensorRev, INPUT);
  randomSeed(analogRead(0));
  digitalWrite(led, LOW);
}

void loop() {
  if (random(0, RAND_PERIOD) == 0) {
      analogWrite(pwm, PWM_VAL);
      digitalWrite(dir, FWD);
      digitalWrite(led, HIGH);
      while(digitalRead(sensorFwd) == HIGH) {
      }
      digitalWrite(led, LOW);
      delay(50);
      digitalWrite(dir, BWD); // reverse for the same amount of time we went forward
      while(digitalRead(sensorRev) == HIGH) {
      }
      analogWrite(pwm, 0);
  }
  delay(1000);
 }
  
