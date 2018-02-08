#include<Servo.h>
Servo eye;
Servo eye_y;
int servoPin = 9;
int servoPin_y = 10;
char received;
String inString;
String inString_y;
float value;
float value_y;
boolean flag= false;

void setup() {
eye.attach(servoPin);
eye_y.attach(servoPin_y);
Serial.begin(9600);
}

void loop() {
  
while (Serial.available() > 0) {
    int inChar = Serial.read();
      // convert the incoming byte to a char and add it to the string:
    if (flag){
       
    inString += (char)inChar;
      
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
      value = inString.toFloat();
      Serial.println(value);
      Serial.println(inString);
      eye.write(value);
      // clear the string for new input:
      inString = "";
    }
  }
}
