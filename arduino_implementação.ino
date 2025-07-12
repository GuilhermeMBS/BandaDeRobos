#include <Servo.h>
#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include <FastLED.h>

/* README
PARA ATIVAR MANDAR NA SERIAL:
  "$acorde"           – o robô faz o movimento de acorde
  "$batida"           – alterna batida de servo e tira de LEDs
  "$batida:<emoção>"  – aciona batida + LEDs com emoção (triste, alegre, raiva, amor)
  "$voz true/false"   – "voz true" levanta o braço, "voz false" abaixa
  "$energia:<0–255>"  – ajusta o brilho do LED do microfone
  "$parar"            – apaga todos os LEDs
  Qualquer texto sem “$” → exibido no LCD
*/

/* DEFINIÇÕES */
#define NUM_LEDS 76
#define LED_PIN   2
#define TIPO      WS2811
#define ORDEM     GRB

/* VARIÁVEIS GLOBAIS */
CRGB leds[NUM_LEDS];
bool estadoLeds = false;
int brilho, R, G, B;

hd44780_I2Cexp lcd;
const int LCD_COLS = 20;
const int LCD_ROWS = 4;

// === Pinos ===
const int servoAcordePin   = 3;
const int servoVozPin      = 10;
const int ledVozPin        = 5;
const int servoBatidaAPin  = 9;
const int servoBatidaBPin  = 6;

// === Servos ===
Servo servoAcorde, servoVoz, servoBatidaA, servoBatidaB;

// === Estados ===
bool estadoAcorde       = false;
bool microfoneLevantado = false;
bool estadoBatida       = false;

void setup() {
  // Inicializa LCD
  int status = lcd.begin(LCD_COLS, LCD_ROWS);
  if (status) hd44780::fatalError(status);

  // Serial + FastLED
  Serial.begin(9600);
  Serial.setTimeout(10);
  FastLED.addLeds<TIPO, LED_PIN, ORDEM>(leds, NUM_LEDS);

  // Anexa servos
  servoAcorde.attach(servoAcordePin);
  servoVoz.attach(servoVozPin);
  servoBatidaA.attach(servoBatidaAPin);
  servoBatidaB.attach(servoBatidaBPin);

  pinMode(ledVozPin, OUTPUT);

  servoVoz.write(microfoneLevantado ? 30 : 0);


  lcd.clear();
  lcd.print("Waiting for song...");
}

void processarComando(String entrada) {
  if (entrada == "acorde") {
    estadoAcorde = !estadoAcorde;
  }
  else if (entrada.startsWith("batida")) {
    // Alterna batida de servo
    estadoBatida = !estadoBatida;
    // Alterna tira de LEDs
    estadoLeds = !estadoLeds;
    if (estadoLeds) {
      // Se veio emoção, aplica cor; senão padrão alegre
      if (entrada.indexOf(':') >= 0) {
        String emoc = entrada.substring(entrada.indexOf(':') + 1);
        emoc.trim();
        if (emoc == "triste")      tristeza();
        else if (emoc == "raiva")  raiva();
        else if (emoc == "amor")   amor();
        else                       alegria();
      } else {
        alegria();
      }
      FastLED.setBrightness(brilho);
    } else {
      parar();
    }
  }
  else if (entrada == "parar") {
    estadoLeds = false;
    parar();
  }
  else if (entrada == "voz true") {
    microfoneLevantado = false;
  }
  else if (entrada == "voz false") {
    microfoneLevantado = true;
  }
  else if (entrada.startsWith("energia:")) {
    String num = entrada.substring(entrada.indexOf(':') + 1);
    num.trim();
    int val = constrain(num.toInt(), 0, 255);
    analogWrite(ledVozPin, val);
  }
}

void atualizarEstados() {
  servoAcorde.write(estadoAcorde ? 30 : 0);
  servoVoz.write(microfoneLevantado ? 30 : 0);
  servoBatidaA.write(estadoBatida ? 90 : 0);
  servoBatidaB.write(estadoBatida ? 90 : 0);
}

void showVerse(const String& verse) {
  lcd.clear();
  for (int i = 0; i < LCD_ROWS; i++) {
    int start = i * LCD_COLS;
    if (start < verse.length()) {
      lcd.setCursor(0, i);
      lcd.print(verse.substring(start, start + LCD_COLS));
    }
  }
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();
    comando.toLowerCase();
    //Serial.println(comando);

    if (comando.startsWith("$")) {
      String cmd = comando.substring(1);
      processarComando(cmd);
      atualizarEstados();
      FastLED.show();
    } else {
      showVerse(comando);
    }
  }
}

// Funções de cor e LED
void parar() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
}

void tristeza() {
  R = rand() % 11;
  G = rand() % 11;
  B = rand() % 56 + 200;
  fill_solid(leds, NUM_LEDS, CRGB(R, G, B));
  brilho = 100;
  FastLED.setTemperature(Candle);
}

void alegria() {
  R = rand() % 128 + 128;
  G = rand() % 128 + 128;
  B = rand() % 51;
  fill_solid(leds, NUM_LEDS, CRGB(R, G, B));
  brilho = 125;
  FastLED.setTemperature(Tungsten100W);
}

void raiva() {
  R = rand() % 56 + 200;
  G = rand() % 11;
  B = rand() % 11;
  fill_solid(leds, NUM_LEDS, CRGB(R, G, B));
  brilho = 175;
  FastLED.setTemperature(Tungsten100W);
}

void amor() {
  R = rand() % 56 + 180;
  G = rand() % 11;
  B = rand() % 56 + 200;
  fill_solid(leds, NUM_LEDS, CRGB(R, G, B));
  brilho = 75;
  FastLED.setTemperature(Candle);
}
