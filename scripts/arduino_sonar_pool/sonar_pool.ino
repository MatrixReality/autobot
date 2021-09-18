//Programa: Coleta dados de um poll de sensores Ultrassonico 
//HC-SR04 e comunica via I2C Arduino e Raspberry Pi (permite 4 sensores)

#include <Wire.h>
#include <Ultrasonic.h>

//Define os pinos para o trigger e echo
#define pino_trigger 4
#define pino_echo 5

//Inicializa o sensor nos pinos definidos acima
Ultrasonic ultrasonic(pino_trigger, pino_echo);

char str[32];
char distance[4];

void setup()
{
  Serial.begin(9600);
  Wire.begin(0x18);
  Wire.onRequest(requestEvent);
}

void requestEvent()
{
  //Le as informacoes do sensor, em cm e pol
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);

  Serial.println("Requisicao recebida!");
  Serial.println(cmMsec);
  
  dtostrf(cmMsec,4,2, distance);
  sprintf(str, "c:%s,l:00.00,r:00.00,b:00.00", distance);
  
  Serial.println(str);
  Wire.write(str);
}

void loop()
{
  delay(1000);
}