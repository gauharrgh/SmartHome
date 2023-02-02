#include "IRremote.h"  // connect the library
#include <Servo.h> 
#define TMP 0 // specify the analog outputs of the Arduino
#define LIGHT 1
#define GAS 2
IRrecv irrecv(2); 
decode_results results;
Servo servo1, servo2, servo3;
int trigPin = 11;	
int echoPin = 12;
int pizo = 3;
int light_pins[]={8,9,4};
void setup() {
  irrecv.enableIRIn(); 
  // enter the initial angle of the servos
  servo1.attach(7);
  servo1.write(0);
  servo2.attach(6);
  servo2.write(180);
  servo3.attach(5);
  servo3.write(0);
  Serial.begin (9600);
// Initialize inputs and outputs
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(TMP, INPUT);
  pinMode(13, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(LIGHT, INPUT);
  pinMode(GAS, INPUT);
  pinMode(pizo, OUTPUT);
  for (int i = 0; i < 3; i++) {
   pinMode(light_pins[i], OUTPUT);
  } }
void loop() {
 // function call
 auto_gate_door();
 delay(250);
 temperature();
 lightning(); 
 gas_control();    }
//gas safety function
void gas_control(){
  float gaslvl;
  gaslvl = analogRead(GAS);
  gaslvl = map(gaslvl,270,700,0,100);
  if(gaslvl >= 10){
     digitalWrite(pizo,HIGH);
  }else digitalWrite(pizo, LOW);
}
// light level function:
void lightning(){
  float lightlvl,state; 
  state = analogRead(LIGHT);
  lightlvl = map(state,344, 1017, 0, 255);
  if(lightlvl>=150){
  for (int i = 0; i < 3; i++) {
   digitalWrite(light_pins[i], HIGH);
  }    }
  if(lightlvl>=80 && lightlvl<150){
   for (int i = 0; i <= 2; i++) {
   digitalWrite(light_pins[i], HIGH);
   if(i==2){digitalWrite(light_pins[i], LOW);} 
  }     }
  if(lightlvl>=5 && lightlvl<80){
  for (int i = 0; i <= 2; i++) {
    if(i==0){digitalWrite(light_pins[i], HIGH);}else{  
      digitalWrite(light_pins[i], LOW);}
  }    }
  if(lightlvl<5){
  for (int i = 0; i < 3; i++) {
   digitalWrite(light_pins[i], LOW);
  }   } }
// temperature and cooling and lighting sensor function
void temperature(){ 
  float celsius;
  celsius = analogRead(TMP);
  celsius = (celsius*5000)/1024;
  celsius = (celsius-500)/10;
  if(celsius>=25.00){ 
    digitalWrite(13,HIGH);
  }else{if(celsius<=25.00){
    digitalWrite(13,LOW);
   } }
  if(celsius<=15.00){ 
    digitalWrite(10,HIGH);
  }else{if(celsius>=15.00){
    digitalWrite(10,LOW);
   } }  };
//gate and door opening function
void auto_gate_door(){
  long duration;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
// Reading data from the ultrasonic sensor: HIGH value, which depends on the duration (in microseconds) between sending an acoustic wave and receiving it back on the echo sounder pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  if(duration > 10000){servo3.write(0);}  
  if ( irrecv.decode( &results )) { 
    switch ( results.value ) {
    case 0xFD08F7:              
        servo1.write(90);
        servo2.write(90);
        break;
    case 0xFD8877:              
        servo1.write(0);
        servo2.write(180);
        break;
    case 0xFD48B7:
      if(duration < 10000){servo3.write(130);};
        break;   }
    irrecv.resume();  } 
