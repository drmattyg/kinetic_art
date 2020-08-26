
#define FWD HIGH
#define BWD LOW
const int sensorFwd = 8;
const int sensorRev = 6;
const int sensorPendulum = 4;
const int pwm =  3;
const int dir = 11;
const int led = 13;
const int RAND_PERIOD = 5;
const int FAILSAFE_DELAY = 500;
const int PWM_FWD = 90;
const int PWM_BWD = 210;
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;
const int DEBOUNCE_COUNT = 3;

void setup() {
  pinMode(pwm, OUTPUT);
  analogWrite(pwm, 0);
  pinMode(dir, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(sensorFwd, INPUT);
  digitalWrite(sensorFwd, HIGH);
  pinMode(sensorRev, INPUT);
  digitalWrite(sensorRev, HIGH);
  pinMode(sensorPendulum, INPUT);
  digitalWrite(sensorPendulum, HIGH);
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

void ramp(int v) {
  int delta = v/3;
  for(int i = 1; i < 4; i++) {
    analogWrite(pwm, delta*i);
    delay(10);
  }
}


bool debounce(int pin) {
  for(int i = 0; i < DEBOUNCE_COUNT; i++) {
    if(digitalRead(pin) == HIGH) {
      return HIGH;
    }
    delay(5);
    return LOW;
  }
}
void loop() {
  if (digitalRead(sensorPendulum) & random(0, RAND_PERIOD) == 0) {
      digitalWrite(dir, FWD);
      ramp(PWM_FWD);
      t0 = millis();
      digitalWrite(led, HIGH);
      while(debounce(sensorFwd) == HIGH) {
        time_delta = millis() - t0;
        if(time_delta > FAILSAFE_DELAY) {
          analogWrite(pwm, 0);
          blink();
        }
      }
      digitalWrite(led, LOW);
      analogWrite(pwm, 0);
      delay(50);
      t0 = millis();
      digitalWrite(dir, BWD); // reverse for the same amount of time we went forward
      ramp(PWM_BWD);
      while(debounce(sensorRev) == HIGH) {
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
  
