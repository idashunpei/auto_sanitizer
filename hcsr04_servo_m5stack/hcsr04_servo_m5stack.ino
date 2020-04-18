// ref: http://www.umek.topaz.ne.jp/mameduino/sonar_howto/

#include <M5Stack.h>
#include <ESP32Servo.h>

#define SERVOPIN 26

#define ECHOPIN 21 // Pin to receive echo pulse (A4pin)
#define TRIGPIN 22 // Pin to send trigger pulse (A5pin)

Servo myservo;
uint16_t color;

void setup(){
//  Serial.begin(9600);
  M5.begin();
  
  pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
  myservo.attach(SERVOPIN);
}

void loop(){
  digitalWrite(TRIGPIN, LOW);// Set the trigger pin to low for 2uS
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);// Send pin low again
  
  int distance = pulseIn(ECHOPIN, HIGH);// Read in times pulse
  distance= distance/58;// Calculate distance from time of pulse

  M5.Lcd.setCursor(10, 10);
  M5.Lcd.setTextSize(3);
  M5.Lcd.print("Distance:");
  M5.Lcd.print(distance);
  M5.Lcd.println(" cm   ");
  
  if (distance < 10) {
    myservo.write(110);
    color = GREEN;
    M5.Lcd.fillCircle(160, 135, 70, GREEN);
  } else {
    myservo.write(10);
    M5.Lcd.fillCircle(160, 135, 70, BLACK);
  }
  
  delay(500); // Wait next ranging
}
