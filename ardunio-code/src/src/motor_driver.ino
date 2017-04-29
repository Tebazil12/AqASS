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

#define DEGREE_ARM 90
#define DEGREE_MAX 180
#define DEGREE_STOP 90
#define DEGREE_MIN 0

#define SPEED_MAX 4
Servo esc;

/** Convert from degrees to m/s */
int degToMPS(int degree){
  //TODO this assumes liniar corelation, check!
  int speed = (degree/float(DEGREE_MAX))*SPEED_MAX; 
  return speed;
}

/** Convert from m/s to degrees */
int mpsToDeg(int speed){//TODO speed needs to be a float!
  //TODO this assumes liniar corelation, check!
  int deg = int((speed/SPEED_MAX)* DEGREE_MAX); 
  return deg;
}

/** Initialize motors */
void initMotor(int pin){
  esc.attach(pin);
  esc.write(DEGREE_ARM);
  delay(5000);
}

/**
 * Take speed in m/s and driver motors at this
 * speed.
 */
void setMotors(int speed){ //TODO speed needs to be a float!
  //int degrees = mpsToDeg(speed);
  esc.write(speed); //degrees);
}

/** Stop the motors. */
void stopMotors(){
  esc.write(DEGREE_STOP);
}

/** Return the maximum speed the motors can go forward in m/s */
int getMaxSpeed(){ //TODO this should be a float
  return degToMPS(DEGREE_MAX);
}

/** Return the maximum speed the motors can go backward in m/s */
int getMinSpeed(){ //TODO this should be a float
  return degToMPS(DEGREE_MIN);
}
