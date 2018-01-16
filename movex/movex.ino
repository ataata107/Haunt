#include<Servo.h>
Servo eye;
int servoPin = 9;
char received;
String inString;
float value;

void setup() {
eye.attach(servoPin);
Serial.begin(9600);
}

void loop() {
  
while (Serial.available() > 0) {
    int inChar = Serial.read();
      // convert the incoming byte to a char and add it to the string:
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
