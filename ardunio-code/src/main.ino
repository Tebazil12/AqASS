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


#include <Arduino.h>
#include <avr/sleep.h>
#include "motor_driver.hpp"
#include "rudder_driver.hpp"
#include "compass_driver.hpp"
#include "serial_comms.hpp"

//#define UNIT_TEST

#define MAX_SERIAL_IN 9 /* The max number of chars that can be read in from the pi*/

#define PIN_MOTORS 9 /* Pin the motors are attached to */
#define PIN_RUDDERS 8 /* Pin the rudders are attached to */

//TODO change to be different for speed and heading!
/* PID constants for Heading */
#define H_KU 0.1 //TODO must experiment and change
#define H_TU 1 //TODO must experiment and change
#define H_KP (0.6*H_KU) //Ziegler–Nichols method
#define H_KI (1.2*H_KU/H_TU) //Ziegler–Nichols method
#define H_KD (3*H_KU*H_TU/40) //Ziegler–Nichols method

/* PID constants for Speed */
#define S_KU 0.01 //TODO must experiment and change
#define S_TU 1 //TODO must experiment and change
#define S_KP (0.6*H_KU) //Ziegler–Nichols method
#define S_KI (1.2*H_KU/H_TU) //Ziegler–Nichols method
#define S_KD (3*H_KU*H_TU/40) //Ziegler–Nichols method

//TODO check if default values make sense //TODO move initialization of values to setup()
int headingDesired; //init in setup
int headingCurrent; // in degrees (min 0, max 359)
int prevHeadErr = 0;
int headingInteg = 0;
int headingBias = 0;

int speedBase = 0; //TODO adjust this
int speedDesired; //init in setup
int speedCurrent; //in m/s - this will only be updated when the pi tells it new info
int speedInteg = 0;//TODO must remember to reset when wildly different desired values
int prevSpeedErr = 0;

float speedFrac = 1; /* Where 1 indicates max speed, 0 stationary */

/**
 * This is a number >= 0 and < 360. When the boat is oriented so the compass
 * is reading 0, the offset should be what bearing the boat is actually facing
 * along according to a calibrated compass.
 */
int compassOffset = 0;

unsigned long timePrev;

/* ***********************FUNCTIONS************************************** */

/* Make sure angle is greater than or equal to 0 and less than 360 */
int wrapHeading(int angle){
  while(angle < 0){ //this seems a little slow/ineligant?
    angle += 360;
  }
  angle = angle % 360;
  return angle;
}

/**
 * Return the angle between the two given headings (in degrees). The angle
 * will always be less than or equal to 180 degrees, and greater than or
 * equal to -180 degrees. Angle will be negative when the second heading is
 * anticlockwise from the first, and positive when clockwise from the first,
 * e.g.:
 *
 *  1st     2nd
 *  \      /
 *   \    /
 *    \__/
 *     \/ <- angle will be +ve

 *  2nd     1st
 *  \      /
 *   \    /
 *    \__/
 *     \/ <- angle will be -ve
 */
int headingDiff(int heading1, int heading2){
  /* Angle is dependant on which quadrant the two headings lie. */
  int angle1 = (360-heading2)+heading1;
  int angle2 = heading2-heading1;
  int angle3 = (360-heading1)+heading2;

  if(abs(angle1)<=abs(angle2) && abs(angle1)<=abs(angle3)){
    return angle1;
  }
  else if (abs(angle2)<=abs(angle1) && abs(angle2) <=abs(angle3)){
    return angle2;
  }
  else if (abs(angle3)<=abs(angle1) && abs(angle3)<=abs(angle2)){
    return angle3;
  }
  else{
    Serial.print("This should be impossible, what did you do?!");
    return 0;
  }
}

/* when theres incoming serial, do this */
void serialEvent(){
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine, MAX_SERIAL_IN);
  int temp;
  switch (nextLine[0]) {//TODO implement all cases
    /* Send current heading */
  case 'c':
    Serial.print("c"); Serial.println(headingCurrent); //is that really the best thing? instead of calling getCompass?
    break;

    /* Update the desiredHeading */
  case 'h':
    temp = getNumber(nextLine);
    if(temp >= 360 || temp < 0){
      Serial.println("n");
    }else{
    headingDesired = temp;
    }
    break;

    /* Update desiredSpeed */
  case 's':
    temp =  getNumber(nextLine);
    if(temp > getMaxSpeed() || temp < getMinSpeed()){
      Serial.println("n");
    }else{
    //speedDesired = temp;
    speedFrac = temp / 100;
    }
    break;

    /* End everything, shutdown */
  case 'e':
    stopMotors();
    stopRudders();
    //Serial.write('e');
    delay(100);
    Serial.println('e');
    delay(100); // to allow time for serial to print
    cli();
    sleep_enable();
    sleep_cpu(); // check this does sleep and never wakes up
    break;

  /* Send current GPS location */
  case 'l':
    break;

  /* Set compass offset */
  case 'o':
    temp =  getNumber(nextLine);
    if(temp >= 360 || temp < 0){
      Serial.println("n");
    }else{
    compassOffset = temp;
    }

    break;

  }
  Serial.print("Current Command:"); Serial.println(nextLine);
  //Serial.println("END_AGAIN");
}

// #ifdef UNIT_TEST
// /* ***************************TESTS************************************** */
// #include <avr/sleep.h> //maybe move this later if used in maincode!
// #include "tests.h"
//
// void setup() {
//     delay(2000); //as suggested when using Unity
//     Serial.begin(9600);
// }
//
// void loop() {
//   runTests();
// }
// #endif

//#ifndef UNIT_TEST
/* ***********************MAIN CODE************************************** */
void setup() {
  Serial.begin(9600);
  initializeCompass();
  setupRudder(PIN_RUDDERS);
  setupMotor(PIN_MOTORS);
  timePrev = millis();
  headingDesired = 90;
  speedDesired =100;
  //set headingDesired to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
}

void loop(){
  //Serial.println("loop");
  /* Refresh values */
  headingCurrent = getCompass() - compassOffset;
  headingCurrent = wrapHeading(headingCurrent);
  Serial.print("d_h: ");Serial.print(headingDesired);
  Serial.print("| a_h: "); Serial.print(headingCurrent);
  unsigned long timeCurrent = millis();
  int timePassed = timeCurrent - timePrev;
  //Serial.print("time since: "); Serial.println(timePassed);

  if(timePassed > 0){/* Handles wrapping of timeCurrent */
    /* PID for Heading */
    int headingError = headingDiff(headingCurrent, headingDesired);
    headingInteg = headingInteg + (headingError * (timePassed/1000));
    headingInteg = constrain(headingInteg, -100, 100); //do not do functions in here, will break! (read docs)
    int headingDeriv = (headingError - prevHeadErr)/(timePassed/1000);
    int rudderAngle = H_KP*headingError + H_KI*headingInteg + H_KD*headingDeriv + headingBias;//bias could be used on the fly to correct for crabbing of boat?
    rudderAngle = constrain(rudderAngle, -90, 90);

    /* PID for Speed */ //TODO is pid really necessary for speed? //TODO slow down at large angle changes to aid small turning circles?//small amount of pid on speed, but when turning, dont pid speed (cuz you cant really)
    int motorSpeed;
    if(abs(headingError) < 45){
      // int speedError = speedDesired - speedCurrent; /* Negative speedError to slow down, positive to speed up */
      // speedInteg = speedInteg + (speedError *(timePassed/1000));//TODO DON'T USE TIME PASSED WHEN ITS NOT UPDATED EVERY LOOP!
      // int speedDeriv = (speedError - prevSpeedErr)/(timePassed/1000);
      // int motorSpeed = S_KP*speedError + S_KI*speedInteg + S_KD*speedDeriv;// + speedBase;
      // motorSpeed = constrain(motorSpeed, -2, 4);
      motorSpeed = int(speedFrac * (getMaxSpeed()-getStopSpeed())); //TODO is this over engineered?
    }else{
      /* Turn a tight corner at half speed to decrease turning circle */
      motorSpeed = int(speedFrac *((getMaxSpeed() - getStopSpeed())/2)); //TODO is this over engineered?
      //if(motorSpeed < 1) motorSpeed = 1; //TODO think about how to not make this go too slow!
      //TODO how to handle resetting values use in PID?
    }
    motorSpeed = constrain(motorSpeed, getMinSpeed() , getMaxSpeed());

    /* Set speed and rudders */
    setRudders(rudderAngle); //rename this to H_TUrn(angle) ? to make this based on angle of boat instead of rudders? (in this case those are ==)
    setMotors(motorSpeed); //rename this to setSpeed(speed) ? so then the driver handles motor speeds
    Serial.print("| set_rudders: "); Serial.print(rudderAngle);

  //  Serial.print("|| d_s: ");Serial.print(speedDesired);
    Serial.print("| a_s: ");Serial.print(speedCurrent);
    Serial.print("| set_speed: "); Serial.println(motorSpeed);

    /* Update values for next iteration */
    prevHeadErr = headingError;
  }
  timePrev = timeCurrent;
  delay(1000);// TODO obviously, reduce this //note, any delay inside this loop will delay reading of next values/
}
//#endif
