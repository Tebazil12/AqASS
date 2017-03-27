#include <Servo.h>
#include <Arduino.h>

#define DEGREE_ARM 90
#define DEGREE_MAX 180
#define DEGREE_STOP 0
#define DEGREE_MIN -10
Servo esc;

/** Converts from degrees to m/s */
int degToMPS(int degrees){
  return degrees; //TODO implement!
}

/** Converts from m/s to degrees */
int mpsToDeg(int speed){
  return speed; //TODO implement!
}

/** Initializes motors */
void setupMotor(int pin){//from Aled's original boat code
  esc.attach(pin);
  esc.write(DEGREE_ARM);
  delay(5000); //TODO use something better than a delay?
}

/**
 * Take speed in m/s and driver motors at this
 * speed.
 *
 */
void setMotors(int speed){
  //TODO clever changing ratio depending on winds, drag etc?
  int degrees = mpsToDeg(speed);
  esc.write(degrees);
}

void stopMotors(){
  esc.write(DEGREE_STOP);
}

int getMaxSpeed(){
  return degToMPS(DEGREE_MAX);
}

int getMinSpeed(){
  return degToMPS(DEGREE_MIN);
}

int getStopSpeed(){
  return degToMPS(DEGREE_STOP);
}
