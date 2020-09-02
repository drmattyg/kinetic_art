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
const int PWM_FWD = 75;
const int PWM_BWD = 210;
const int DEMO_WAIT_TIME = 1000*12;
const int DEMO_REPEAT = 3;
unsigned long t0;
unsigned long time_delta;
int buttonState = 0;
const int DEBOUNCE_COUNT = 3;

void setup() {
  analogWrite(pwm, 0);
  pinMode(pwm, OUTPUT);
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

void blink1() {
  while(true) {
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    delay(100);
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    delay(500);
  }
}

void ramp(int v) {
  int delta = v/3;
  for(int i = 1; i < 4; i++) {
    analogWrite(pwm, delta*i);
    delay(20);
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
  bool first = true;
  for(int i = 0; i < DEMO_REPEAT; i++) {
    while(digitalRead(sensorPendulum) & ~first) {
      first = false;
      // wait for pendulum to center
    }
    digitalWrite(dir, FWD);
    delay(1000);
    ramp(90);
    while(digitalRead(sensorFwd) == HIGH) {
      
    }
    analogWrite(pwm, 0);
    delay(500);
    digitalWrite(led, HIGH);
    digitalWrite(dir, BWD);
    ramp(180);
    while(digitalRead(sensorRev) == HIGH) {
      
    }
    analogWrite(pwm, 0);
    digitalWrite(led, LOW);
    delay(DEMO_WAIT_TIME);
 }
 blink1();
}
  
