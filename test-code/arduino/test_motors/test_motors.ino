#include <Servo.h>

Servo motors;
Servo rudders;

void setup(){
  //A2 motors
  //A3 rudders
  motors.attach(A2);
  motors.write(90);
  
  rudders.attach(A3);
  rudders.write(90);
  
  delay(5000);
}

void loop(){
  //full left/ forward
  motors.write(135); //150 ==-30 degrees, 120==-15
  delay(2000);
  //center /stop
  motors.write(90);
  delay(3000);
  //full right / backward
 /* motors.write(135); //30 ==30degrees, 60==15
  delay(2000);
  //center /stop
  motors.write(90);
  delay(1000);*/
}
