
#define FWD HIGH
#define BWD LOW

const int sensorPin = 2;
const int relay1 =  12;
const int relay2 = 11;
int buttonState = 0;

void setup() {
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(sensorPin, INPUT);
}

void loop() {
  buttonState = digitalRead(sensorPin);

  // check if the pushbutton is pressed. If it is, the sensorState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, LOW);
  } else {
    // turn LED off:
    digitalWrite(relay1, LOW);
    digitalWrite(relay2, HIGH);
  }
}