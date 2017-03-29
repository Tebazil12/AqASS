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
