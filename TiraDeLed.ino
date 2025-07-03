/*BIBLIOTECAS*/
# include <FastLED.h>


/*DEFINIÇÕES*/
# define NUM_LEDS 76  // número de leds na tira
# define LED_PIN 2    // pino de conexão do arduino
# define TIPO WS2811  // tipo de fita de led
# define ORDEM GRB    // ordem padrão do FastLED

/*OBSERVAÇÕES*/
/*
para definir novas cores, basta fazer combinações de diferentes quantidades das primárias

CRGB(255, 0, 0);       VERMELHO
CRGB(0, 255, 0);       VERDE
CRGB(0, 0, 255);       AZUL
CRGB(255, 255, 0);     AMARELO
CRGB(255, 0, 255);     ROSA
CRGB(0, 255, 255);     CIANO
CRGB(255, 255, 255);   BRANCO


fill_solid | altera a cor de todos os leds da fita simultaneamente
for (int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB(x, y, z); } | percorre os leds da fita, alterando a cor um por um

v1 = rand() % 100;         | v1 RNG de 0 a 99
v2 = rand() % 100 + 1;     | v2 RNG de 1 a 100
v3 = rand() % 30 + 1985;   | v3 RNG de 1985-2014

*/

/*VARIÁVEIS GLOBAIS*/
CRGB leds[NUM_LEDS];  // fita de led

bool estadoLeds = false;  // estado dos leds (aceso/apagado)

int brilho, R, G, B;  // R, G, B são quantidades variáveis de cor associadas a uma emoção

/* FUNÇÕES */
void parar() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
}

void tristeza() {
  R = rand() % 11;
  G = rand() % 11;
  B = rand() % 56 + 200;
  for (int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB(R, G, B); }
  brilho = 100;
  FastLED.setTemperature(Candle);
}

void alegria() {
  R = rand() % 128 + 128;
  G = rand() % 128 + 128;
  B = rand() % 51;
  for (int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB(R, G, B); }
  brilho = 125;
  FastLED.setTemperature(Tungsten100W);
}

void raiva() {
  R = rand() % 56 + 200;
  G = rand() % 11;
  B = rand() % 11;
  for (int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB(R, G, B); }
  brilho = 175;
  FastLED.setTemperature(Tungsten100W);
}

void amor() {
  R = rand() % 56 + 180;
  G = rand() % 11;
  B = rand() % 56 + 200;
  for (int i = 0; i < NUM_LEDS; i++) { leds[i] = CRGB(R, G, B); }
  brilho = 75;
  FastLED.setTemperature(Candle);
}

/* SETUP & LOOP */
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  FastLED.addLeds<TIPO, LED_PIN, ORDEM>(leds, NUM_LEDS);
 
}

void loop() {
  if (Serial.available() > 0) { // verificando se há dados disponíveis para serem lidos na porta serial.

    String texto = Serial.readStringUntil('\n');
    texto.trim();

    String trecho1 = texto.substring(0, 6);  // simula detecção de batida

    String trecho2 = texto.substring(7);     // pega a emoção da batida

    if (trecho1 == "batida") {

      estadoLeds = !estadoLeds;

      if (estadoLeds) {
        FastLED.setBrightness(brilho);
      } else {
        FastLED.setBrightness(30);
      }
      if (trecho2 == "triste") { tristeza(); }
      else if (trecho2 == "alegre") { alegria(); }
      else if (trecho2 == "raiva") { raiva(); }
      else if (trecho2 == "amor") { amor(); }
    }

    if (texto == "parar") { parar(); }
 
    FastLED.show();
  }
}
