#include <Servo.h>
/*README
PARA ATIVAR MANDAR NA SERIAL:
"batida", cada vez que voce mandar "batida" o robo fara um movimento
"acorde", cada vez que voce mandar "acorde" o robo fara um movimento
"voz", esse é um pouco diferente, existe 2 tipos de comando o "voz true/false" e o "voz(num)" o primeiro sendo para ligar e desligar o led e o segundo para a intensidade
*/


// === Pinos ===
const int servoAcordePin = 3;
const int servoVozPin = 5;
const int ledVozPin = 6;           // pino digital PWM
const int servoBatidaAPin = 9;
const int servoBatidaBPin = 10;

// === Servos ===
Servo servoAcorde;
Servo servoVoz;
Servo servoBatidaA;
Servo servoBatidaB;

// === Estados ===
bool estadoAcorde = false;
bool microfoneLevantado = false;
bool estadoBatida = false;

void setup() {
  Serial.begin(9600);

  servoAcorde.attach(servoAcordePin);
  servoVoz.attach(servoVozPin);
  servoBatidaA.attach(servoBatidaAPin);
  servoBatidaB.attach(servoBatidaBPin);

  pinMode(ledVozPin, OUTPUT);

  Serial.println("Comandos:");
  Serial.println("- acorde");
  Serial.println("- batida");
  Serial.println("- voz true / voz false");
  Serial.println("- voz:<intensidade>  (0–255)");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    processarComando(comando);
  }

  atualizarEstados();
}

void processarComando(String entrada) {
 
  entrada.toLowerCase();

  if (entrada == "acorde") {
    estadoAcorde = !estadoAcorde;
  } 
  else if (entrada == "batida") {
    estadoBatida = !estadoBatida;
  }
  else if (entrada == "voz true") {
    microfoneLevantado = true;
  } 
  else if (entrada == "voz false") {
    microfoneLevantado = false;
  }
  else if (entrada.startsWith("voz:")) {
    entrada.replace("voz:", "");
    entrada.trim();
    int intensidade = entrada.toInt();
    intensidade = constrain(intensidade, 0, 255);
    analogWrite(ledVozPin, intensidade);
    Serial.println("Intensidade do LED: " + String(intensidade));
  }

  Serial.println("Executado: " + entrada);
}

void atualizarEstados() {
  // Robô "acorde"
  servoAcorde.write(estadoAcorde ? 90 : 0);

  // Robô "voz"
  servoVoz.write(microfoneLevantado ? 90 : 0);

  // Robô "batida"
  if (estadoBatida) {
    servoBatidaA.write(60);
    servoBatidaB.write(120);
  } else {
    servoBatidaA.write(0);
    servoBatidaB.write(0);
  }
}
