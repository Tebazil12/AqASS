#include <Servo.h>
Servo rudder; //see if there is a better place to put this

void setupRudder(){
  rudder.attach(8); // servo is attached to pin 8
}

/**
 * This should correspond to the angle you want the rudders set at,
 * with 0 setting the boat to go straight forward, -90 should turn the
 * boat fully to the left, and 90 should turn the boat fully to the right.
 */
void setRudders(int angle){


}
