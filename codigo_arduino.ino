#include <ESP32Servo.h>

// Pines anteriores
int pinAzul = 14; 
int pinRojo = 15;
int pinBoton = 13;

// Configuración del Servo
Servo miServo;
int pinServo = 12;

void setup() {
  Serial.begin(115200);
  
  pinMode(pinAzul, OUTPUT);
  pinMode(pinRojo, OUTPUT);
  pinMode(pinBoton, INPUT_PULLUP);
  
  // Inicializar Servo
  ESP32PWM::allocateTimer(0); // Necesario para algunas placas ESP32
  miServo.setPeriodHertz(50); // Servo estándar de 50Hz
  miServo.attach(pinServo, 500, 2400); // Attach del servo
  
  miServo.write(0); // Empezamos en 0 grados (Cerrado)
}

void loop() {
  // 1. Botón
  if (digitalRead(pinBoton) == LOW) {
    Serial.println("SOLICITUD");
    delay(400);
  }

  // 2. Respuesta de Python
  if (Serial.available() > 0) {
    char dato = Serial.read();
    
    if (dato == '1') { // ACCESO CONCEDIDO
      digitalWrite(pinAzul, HIGH);
      miServo.write(90);  // GIRA A 90 GRADOS
      delay(5000);        // Espera 5 segundos
      miServo.write(0);   // REGRESA A 0 GRADOS
      digitalWrite(pinAzul, LOW);
    } 
    else if (dato == '0') { // ACCESO DENEGADO
      digitalWrite(pinRojo, HIGH);
      delay(2000); 
      digitalWrite(pinRojo, LOW);
    }
  }
}