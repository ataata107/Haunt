#include<Servo.h>
Servo eyex;
Servo eyey;
int servoPinx = 9;
int servoPiny = 10;
char received;
String inString,servo1,servo2;
float value,n1,n2;


void setup() {
eyex.attach(servoPinx);
eyey.attach(servoPiny);
Serial.begin(9600);
}

void loop() {
  
while (Serial.available() > 0) {
    int inChar = Serial.read();
      // convert the incoming byte to a char and add it to the string:
    inString += (char)inChar;
    
    // if you get a newline, print the string, then the string's value:
//    if (inChar == '\a') {
//      value = inString.toFloat();
//      Serial.println(value);
//      Serial.println(inString);
//      eyex.write(value);
//      // clear the string for new input:
//      inString = "";
//    }
    if (inChar == '\n') {
      
      servo1 = inString.substring(0, 5); //get the first four characters
      servo2 = inString.substring(5,10); //get the next four characters 
      Serial.println("Hello World");
      Serial.println(servo1);  //print to serial monitor to see parsed results
      Serial.println(servo2);

      int n1 = servo1.toFloat();
      int n2 = servo2.toFloat();

      Serial.println("the numbers are :");
      Serial.println(n1);  //print to serial monitor to see number results
      Serial.println(n2);
            
      eyex.write(n1); //set servo position 
      eyey.write(n2);
      inString="";
      
      
//      value = inString.toFloat();
//      Serial.println(value);
//      Serial.println(inString);
//      eyey.write(value);
//      // clear the string for new input:
//      inString = "";
    }
    
  }
}
