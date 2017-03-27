#include <Servo.h>

#define MAX_VALUE 180 /* The max raw value that can be sent to rudders*/
#define MIN_VALUE 0 /* The min raw value that can be sent to rudders*/
#define CENTER_VALUE 90 /* The raw value that sets the rudders to go straight */

Servo rudder; //see if there is a better place to put this

void setupRudder(int pin){
  rudder.attach(pin);
}

/* Covert from what the main code expects (angle of rudder in degrees) to raw rudder values */
int softToDeg(int angle){
  return angle+90;
}

/* Covert from raw rudder values to what the main code expects (angle of rudder in degrees) */
int rawToDeg(int value){
  return value-90;
}

/**
 * Corresponds to the angle you want the rudders set at,
 * with 0 setting the boat to go straight forward, -90 should turn the
 * rudders fully to the left, and 90 should turn the rudders fully to the right.
 *
 * With this boat, the rudders will turn to a max of ~45 degrees in either
 * direction, not 90 degrees.
 */
void setRudders(int angle){
  int raw = softToDeg(angle);
  rudder.write(raw);
}

/**
 * Center the rudders and detach them.
 * This should only be used at the end of the program!
 */
void stopRudders(){
  rudder.write(CENTER_VALUE);
  rudder.detach();
}

int getHardLeft(){
  return rawToDeg(MAX_VALUE);
}

int getHardRight(){
  return rawToDeg(MIN_VALUE);
}

int getCenter(){
  return rawToDeg(CENTER_VALUE);
}
