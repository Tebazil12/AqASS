/*Copyright (c) 2017 Lizzie Stone
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.*/

#define MAX_VALUE 150   /* The max raw value that can be sent to rudders */
#define MIN_VALUE 30    /* The min raw value that can be sent to rudders */
#define CENTER_VALUE 90 /* The raw value that sets the rudders to go straight */

Servo rudder;

/** Initialize servos by attaching to pin, and set them to point dead ahead */
void initRudder(int pin){
  rudder.attach(pin);
  rudder.write(CENTER_VALUE);
}

/**
 * Covert from what the main code expects (angle of rudder in degrees) to raw
 * rudder values 
 */
int degToRaw(int angle){
  return 180-(angle+90);
}

/**
 * Covert from raw rudder values to what the main code expects (angle of 
 * rudder in degrees) 
 */
int rawToDeg(int value){
  return (180-value)-90;
}

/**
 * Corresponds to the angle you want the rudders set at,
 * with 0 setting the boat to go straight forward, -90 should turn the
 * rudders fully to the left, and 90 should turn the rudders fully to 
 * the right.
 *
 * With this boat, the rudders will turn to a max of ~45 degrees in either
 * direction, not 90 degrees.
 *
 *   _      _      _
 *  / \    / \    / \
 * /   \  /   \  /   \
 * |   |  |   |  |   |
 * |   |  |   |  |   |
 * |___|  |___|  |___|
 *   /      |      \
 *  Left  Center Right
 *  (-30)  (0)    (30)
 */
void setRudders(int angle){
  int raw = degToRaw(angle);
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

/* Return the lowest (left most) angle that the rudders can be set at */
int getHardLeft(){
  return rawToDeg(MAX_VALUE);
}

/* Return the highest (right most) angle that the rudders can be set at */
int getHardRight(){
  return rawToDeg(MIN_VALUE);
}

