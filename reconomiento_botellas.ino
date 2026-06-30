#include <Servo.h>

const int RED_LED_PIN   = 8;   
const int GREEN_LED_PIN = 9;   
const int SERVO_PIN     = 10;  

const int SERVO_ANGLE_OBJECT   = 90;  
const int SERVO_ANGLE_NO_OBJECT = 0;  

Servo myServo;

void setup() {
  Serial.begin(9600);

  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);

  myServo.attach(SERVO_PIN);

  digitalWrite(RED_LED_PIN, HIGH);
  digitalWrite(GREEN_LED_PIN, LOW);
  myServo.write(SERVO_ANGLE_NO_OBJECT);
}

void loop() {

  if (Serial.available() > 0) {
    char command = Serial.read();

    while (Serial.available() > 0) {
      Serial.read();
    }

    if (command == 'A') {
      digitalWrite(GREEN_LED_PIN, HIGH);
      digitalWrite(RED_LED_PIN, LOW);
      myServo.write(SERVO_ANGLE_OBJECT);
    } 
    else if (command == 'B') {

      digitalWrite(RED_LED_PIN, HIGH);
      digitalWrite(GREEN_LED_PIN, LOW);
      myServo.write(SERVO_ANGLE_NO_OBJECT);
    }
  }
}