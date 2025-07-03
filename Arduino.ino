void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    String texto = Serial.readStringUntil('\n');
    Serial.println(texto + " copiado");
  }
}
