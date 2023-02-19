#include <math.h>

int pump=3, peltier=4, fan=5, ntc1=6, ntc2=7;
int fanT=74;
int tankT=74; 
int measureTemps=0, holder=0, okuTank, okuFan;
int tempC, tempK, tempCtank, tempCfan;
char message;
void setup() {
  pinMode(pump,OUTPUT);
  pinMode(peltier,OUTPUT);
  pinMode(fan,OUTPUT);
  pinMode(ntc1,OUTPUT);
  pinMode(ntc2,OUTPUT);
  Serial.begin(4800);
}
//double Termistor(int analogOkuma){
//  tempK = log(((1024000 / analogOkuma) - 10000));
//  tempK = 1/(0.001129148 + (0.000234125 + (0.0000000876741 * tempK  * tempK))*tempK);
//  tempC = tempK - 273.15;
//  return tempC;  
//}

void loop() 
{
  // 10 ms lik aralarla okutuyorum ki başka bir emir gelirse delay komutunun bitmesini uzun süre beklemesin
  delay(10);
  holder = holder + 10;
  if (holder == 1000)
  {
    //okuTank = analogRead(A0);
    //okuFan = analogRead(A1);
    //tempCtank = Termistor(okuTank);
    //tempCfan = Termistor(okuFan);
    
    tempCtank = analogRead(A0);
    tempCfan = analogRead(A1);
    
    Serial.print("tank");
    Serial.print(" ");
    if ( measureTemps == 1){
      Serial.print(tempCtank); }
    else if ( measureTemps == 0){ 
      Serial.print("okunamadi");      
    }
    Serial.print(" ");
    Serial.print("fan");
    Serial.print(" ");
    if ( measureTemps == 1){
      Serial.println(tempCfan); }
    else if ( measureTemps == 0){ 
      Serial.println("okunamadi");      
    }
    holder = 0;
  }
  if(Serial.available()>0)
  {
    message = Serial.read();
    if(message == '1')
    {
      digitalWrite(pump,HIGH);
      Serial.println("ProMini: Pump is working!");
    }
    if(message == '2')
    {
      digitalWrite(pump,LOW);
      Serial.println("ProMini: Pump stopped!");
    }
    if(message == '3')
    {
      digitalWrite(peltier,HIGH);
      Serial.println("ProMini: Peltier is enabled!");
    }
    if(message == '4')
    {
      digitalWrite(peltier,LOW);
      Serial.println("ProMini: Peltier is disabled!");
    }
    if(message == '5')
    {
      digitalWrite(fan,HIGH);
      Serial.println("ProMini: Fan was started!");
    }
    if(message == '6')
    {
      digitalWrite(fan,LOW);
      Serial.println("ProMini: Fan was stopped!");
    }
    if(message == '7')
    {
      Serial.println("ProMini: - Temperatures are sending!");
      digitalWrite(ntc1,HIGH);
      digitalWrite(ntc2,HIGH);
      measureTemps = 1;
    }
    if(message == '8')
    {
      digitalWrite(ntc1,LOW);
      digitalWrite(ntc2,LOW);
      measureTemps = 0;
      Serial.println("ProMini: - Temperatures sending disabled!");
    }
    
  }
}
