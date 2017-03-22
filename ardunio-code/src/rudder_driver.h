#include <Servo.h>
Servo rudder; //see if there is a better place to put this

void setupRudder(int pin){
  rudder.attach(pin); // servo is attached to pin 8
}

/**
 * This should correspond to the angle you want the rudders set at,
 * with 0 setting the boat to go straight forward, -90 should turn the
 * boat fully to the left, and 90 should turn the boat fully to the right.
 */
void setRudders(int angle){
  rudder.write(angle-90);//test this on boat, make sure things go in correct directions

}

void stopRudders(){
  rudder.write(0);
  rudder.detach(); //this is to stop power being used
}
