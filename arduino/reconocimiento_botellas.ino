#include <Servo.h>

Servo miServo;

// Pines LED RGB
const int rojo = 9;
const int verde = 10;
const int azul = 11;

// Posición inicial del servo
int posicion = 90;

void setup() {
  // Configurar LED RGB
  pinMode(rojo, OUTPUT);
  pinMode(verde, OUTPUT);
  pinMode(azul, OUTPUT);

  // Configurar servo
  miServo.attach(6);
  miServo.write(90);
}

void loop() {

  // ROJO + Servo a 90°
  digitalWrite(rojo, HIGH);
  digitalWrite(verde, LOW);
  digitalWrite(azul, LOW);

  miServo.write(90);
  delay(2000);

  // AZUL + Servo a 180°
  digitalWrite(rojo, LOW);
  digitalWrite(verde, LOW);
  digitalWrite(azul, HIGH);

  miServo.write(180);
  delay(2000);

  // VERDE + Servo a 90°
  digitalWrite(rojo, LOW);
  digitalWrite(verde, HIGH);
  digitalWrite(azul, LOW);

  miServo.write(90);
  delay(2000);
}
