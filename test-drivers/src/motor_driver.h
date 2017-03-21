#include <Servo.h>
#define ARM_ESC 80
Servo esc;

void setupMotor(int pin){//from Aled's original boat code
  esc.attach(pin);  //esc is attached to pin 9
  esc.write(ARM_ESC); //this is the value that will arm the ESC (needs tinkering)
}

/**
 * Take speed in m/s and driver motors at this
 * speed.
 *
 */
 void setMotors(int speed){
//clever changing ratio depending on winds, drag etc?

  esc.write(speed);

}

void stopMotors(){
  esc.write(0);
}
