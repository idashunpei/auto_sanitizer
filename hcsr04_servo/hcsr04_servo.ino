// ref: http://www.umek.topaz.ne.jp/mameduino/sonar_howto/

#include <Servo.h>

#define ECHOPIN 18 // Pin to receive echo pulse (A4pin)
#define TRIGPIN 19// Pin to send trigger pulse (A5pin)

Servo myservo;

void setup(){
  Serial.begin(9600);
  pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
  myservo.attach(9);
}

void loop(){
  digitalWrite(TRIGPIN, LOW);// Set the trigger pin to low for 2uS
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);// Send pin low again
  
  int distance = pulseIn(ECHOPIN, HIGH);// Read in times pulse
  distance= distance/58;// Calculate distance from time of pulse
  
  Serial.print("Distance:");
  Serial.print(distance);
  Serial.println(" cm");
  
  if (distance < 10) {
    myservo.write(10);
  } else {
    myservo.write(180);
  }
  
  delay(500); // Wait next ranging
}
