#include <Servo.h>
Servo haunting_eye;

void setup() {
  Serial.begin(9600);
  haunting_eye.attach(9);
  haunting_eye.write(90);
}
 
float integerValue=0;  // Max value is 65535
float decimalValue=0;
int n;
char incomingByte;
 
void loop() {
  if (Serial.available() > 0) {   // something came across serial
    integerValue = 0;     // throw away previous integerValue
    decimalValue = 0;
    n=1;
    while(1) {            // force into a loop until 'n' is received
      incomingByte = Serial.read();
      if (incomingByte == '\n') break;   // exit the while(1), we're done receiving
      if (incomingByte == -1) continue;  // if no characters are in the buffer read() returns -1
      if (incomingByte == '.'){
        while(1){
          incomingByte = Serial.read();
          if (incomingByte == '\n') break;
          
          decimalValue *= 10;
          
          decimalValue = ((incomingByte - 48) + decimalValue);
          
          n=n+1;
        }
        (integerValue) = (integerValue) + (decimalValue)/pow(10,n);
        break;
      }
      integerValue *= 10;  // shift left 1 decimal place
      // convert ASCII to integer, add, and shift left 1 decimal place
      integerValue = ((incomingByte - 48) + integerValue);
    }
    Serial.println(integerValue);   // Do something with the value
    haunting_eye.write(integerValue);
  }
}
