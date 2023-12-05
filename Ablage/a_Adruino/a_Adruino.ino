#include <Wire.h>
//istVL, istRL, istInk, istVakuum, istDruck, vorVakuum
int istVL = A0;
int istRL = A1;
int istPumpe = 5;
int istVakuum = A2;
int istDruck = A3;
int vorVakuum = A6;

void setup() {
  //Serial.begin(115200);
  pinMode(istVL, INPUT);
  pinMode(istRL, INPUT);
  pinMode(istPumpe, INPUT);
  pinMode(istVakuum, INPUT);
  pinMode(istDruck, INPUT);
  pinMode(vorVakuum, INPUT);

  Wire.begin(0x40);
  Wire.onRequest(antwortfunktion);

}

int frequenzMessung(int eingang) {
  float zeit = 0;
  float frequenz = 0;
  int umlauf = 1;
  for (int i = 0; i < umlauf; i++) {
    float zeitMinus = pulseIn(eingang, LOW);
    float zeitPlus = pulseIn(eingang, HIGH);
    /*Serial.println(zeitMinus);
      Serial.println(zeitPlus);
      Serial.println();*/
    zeit += zeitMinus + zeitPlus;
  }
  zeit = zeit / umlauf;
  if (zeit > 0) {
    //Serial.println(String(zeit) + "------------------------------------------------------");
    frequenz = 1000000 / zeit;
  }
  else {
    frequenz = 0;
  }
  //Serial.println(frequenz);
  return int (frequenz);
}
/*
int spannungsMessung(int eingang) {            //zum Testen vom Spannungseingang
  int umlauf = 1000;
  float spannung = 0;
  for (int i = 0; i < umlauf; i++) {
    float wert = analogRead(eingang);
    spannung += wert;
    //Serial.println(spannung);
  }
  spannung = spannung / umlauf;
  return spannung;
}*/

void loop()
{

  //Serial.println(frequenzMessung(istVakuum));
  //delay(10);


}

void antwortfunktion() {
  byte buffer[11];  //istVL, istRL, istInk, istVakuum, istDruck, vorVakuum
    buffer[0] = highByte(analogRead(istVL));
    buffer[1] = lowByte(analogRead(istVL));
    buffer[2] = highByte(analogRead(istRL));
    buffer[3] = lowByte(analogRead(istRL));
    int istPumpeZeit = frequenzMessung(istPumpe);
    buffer[4] = highByte( istPumpeZeit);
    buffer[5] = lowByte( istPumpeZeit);
    buffer[6] = highByte(analogRead(istVakuum));
    buffer[7] = lowByte(analogRead(istVakuum));
    buffer[8] = highByte(analogRead( istDruck));
    buffer[9] = lowByte(analogRead( istDruck));
    buffer[10] = highByte(analogRead(vorVakuum));
    buffer[11] = lowByte(analogRead(vorVakuum));

  Wire.write(buffer, 12);
  //Serial.println('I2C - send from Arduino');
}
