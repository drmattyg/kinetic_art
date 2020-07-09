
#define FWD HIGH
#define BWD LOW
const int sensorFwd = 8;
const int sensorRev = 6;
const int pwm =  3;
const int dir = 11;
const int led = 13;
const int RAND_PERIOD = 10; // 20 seconds
const int FAILSAFE_DELAY = 1500;
int PWM_VAL = 130;
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

void blink() {
  while(true) {
    digitalWrite(led, HIGH);
    delay(250);
    digitalWrite(led, LOW);
    delay(250);
  }
}

void loop() {
  if (random(0, RAND_PERIOD) == 0) {
      analogWrite(pwm, PWM_VAL);
      t0 = millis();
      digitalWrite(dir, FWD);
      digitalWrite(led, HIGH);
      while(digitalRead(sensorFwd) == HIGH) {
        time_delta = millis() - t0;
        if(time_delta > FAILSAFE_DELAY) {
          analogWrite(pwm, 0);
          blink();
        }
      }
      digitalWrite(led, LOW);
      delay(50);
      t0 = millis();
      digitalWrite(dir, BWD); // reverse for the same amount of time we went forward
      while(digitalRead(sensorRev) == HIGH) {
        time_delta = millis() - t0;
        if(time_delta > FAILSAFE_DELAY) {
          analogWrite(pwm, 0);
          blink();
        }
      }
      analogWrite(pwm, 0);
  }
  delay(1000);
 }
  
