
#define FWD HIGH
#define BWD LOW
const int sensorFwd = 8;
const int sensorRev = 6;
const int sensorPendulum = 4;
const int pwm =  3;
const int dir = 11;
const int led = 13;
const int RAND_PERIOD = 2;
const int FAILSAFE_DELAY = 1500;
const int PWM_FWD = 150;
const int PWM_BWD = 200;
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;
const int DEBOUNCE_COUNT = 3;
const int PWM_RAMP_COUNT = 4;
const int PWM_RAMP_DELAY = 10;

void setup() {
  pinMode(pwm, OUTPUT);
  analogWrite(pwm, 0);
  pinMode(dir, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(sensorFwd, INPUT);
  pinMode(sensorRev, INPUT);
  pinMode(sensorPendulum, INPUT);
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

void rampPWMUp(int val) {
  int delta = val/PWM_RAMP_COUNT;
  int pwm_val = 0;
  while(pwm_val < val) {
    pwm_val += delta;
    if(pwm_val > val) {
      pwm_val = val;
    }
    analogWrite(pwm, pwm_val);
    delay(PWM_RAMP_DELAY);
  }
}

void rampPWMDown(int currVal) {
  int delta = currVal/PWM_RAMP_COUNT;
  int pwm_val = currVal;
  while(pwm_val > 0) {
    pwm_val -= delta;
    if(pwm_val < 0) {
      pwm_val = 0;
    }
    analogWrite(pwm, pwm_val);
    delay(PWM_RAMP_DELAY);
  }
}

bool debounce(int pin) {
  for(int i = 0; i < DEBOUNCE_COUNT; i++) {
    if(digitalRead(pin) == HIGH) {
      return HIGH;
    }
    return LOW;
  }
}
void loop() {
  if (digitalRead(sensorPendulum) & random(0, RAND_PERIOD) == 0) {
      digitalWrite(dir, FWD);
      analogWrite(pwm, PWM_FWD);
      t0 = millis();
      digitalWrite(led, HIGH);
      while(digitalRead(sensorFwd) == HIGH) {
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
      analogWrite(pwm, PWM_BWD);
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
  
