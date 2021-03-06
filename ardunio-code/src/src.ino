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
#include <Wire.h>
#include <Servo.h>
#include "Adafruit_Sensor.h"
#include "Adafruit_HMC5883_U.h"

/* Uncomment this to enable print out - WILL DISRUPT COMMS WITH PI */
//#define DEBUG_PRINT 

#define MAX_SERIALIN 9  /* The max number of chars that can be read in from the pi*/

#define PIN_MOTORS A2   /* Pin the motors are attached to */
#define PIN_RUDDERS A3  /* Pin the rudders are attached to */

/* PID constants for Heading */
#define KU 1 //TODO must experiment and change
#define TU 1 //TODO must experiment and change
#define KP 2//(0.6*KU)      //Ziegler–Nichols method
#define KI 0 //(1.2*KU/TU)  //Ziegler–Nichols method
#define KD 0 //(3*KU*TU/40) //Ziegler–Nichols method

int headDesired; /* in degrees, min 0, max 359 */
int headCurrent; /* in degrees, min 0, max 359 */
int prevHeadErr;
int headInteg;
int headBias;

int fullSpeed;
int halfSpeed;
float speedFrac = 1; /* Where 1 indicates max speed, 0 stationary */

/**
 * This is a number >= 0 and < 360. When the boat is oriented so the compass
 * is reading 0, the offset should be what bearing the boat is actually facing
 * along according to a calibrated compass.
 */
int compassOffset = 0;

unsigned long timePrev;

/* ***********************FUNCTIONS************************************** */

/** Wrap angle to be between 0 and 359 */
int wrapHeading(int angle){
  while(angle < 0){
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
int headDiff(int head1, int head2){
  /* Angle is dependant on which quadrant the two headings lie. */
  int angle1 = (head2-360)-head1;
  int angle2 = head2-head1;
  int angle3 = (360-head1)+head2;

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
    #ifdef DEBUG_PRINT
    Serial.print("This should be impossible, what did you do?!");
    #endif
    return 0;
  }
}

/**
 * When theres incoming serial, do this after current itteration of loop().
 * Reads the incoming serial and interperates the message. 
 * This Recognises four commands:
 * 
 * c - send the current heading
 * e - shut down
 * h(xxx) - replace the desired heading with the new heading xxx
 * o(xxx) - replace the compass offset with the new offset xxx
 *
 * This sends the following commands:
 *
 * e - signals the shutdown command was registered
 *
 * This code was adapted from 
 * https://github.com/abersailbot/dewi-arduino/blob/master/src/dewi.ino
 */
void serialEvent(){
  
  char nextLine[MAX_SERIALIN+1];
  readSerialLine(nextLine, MAX_SERIALIN);
  int temp;
  
  switch (nextLine[0]) {
  
  /* Send current heading */
  case 'c':
    Serial.print("c("); Serial.print(headCurrent);Serial.println(")");
    break;

  /* Update the desiredHeading */
  case 'h':
    temp = getNumber(nextLine);
    if(temp >= 360 || temp < 0){
     // Serial.println("x"); /* Send error message to Pi */
    }else{
    headDesired = temp;
    }
    break;

  /* End everything, shutdown */
  case 'e':
    stopMotors();
    stopRudders();
    delay(100);
    Serial.println('e');
    delay(100); // to allow time for serial to print
    cli();
    sleep_enable();
    sleep_cpu();
    break;

  /* Set compass offset */
  case 'o': 
    temp =  getNumber(nextLine);
    if(temp >= 360 || temp < 0){
     // Serial.println("x");/* Send error message to Pi */
    }else{
    compassOffset = temp;
    }
    break;
    
  /* Unrecognised Command */
  //default:
   // Serial.println("x");
  
  }
  
  #ifdef DEBUG_PRINT
  Serial.print("Current Command:"); Serial.println(nextLine);
  #endif
}

/* ***********************MAIN CODE************************************** */
void setup() {
  
  Serial.begin(9600);
  delay(1000); /* So code doesn't run when reprogramming */
  
  initCompass();
  initRudder(PIN_RUDDERS);
  initMotor(PIN_MOTORS);
  
  timePrev = millis();
  
  headDesired = 90;
  prevHeadErr = 0;
  headInteg = 0;
  headBias = 0;
  
  fullSpeed =  150;// int(speedFrac * getMaxSpeed());
  halfSpeed = 120;// int(speedFrac *(getMaxSpeed()/2));
}

void loop(){
  #ifdef DEBUG_PRINT
  Serial.println("loop");
  #endif
  
  /* Refresh values */
  headCurrent = getCompass() - compassOffset;
  headCurrent = wrapHeading(headCurrent);
    
  unsigned long timeNow = millis();
  int timePassed = timeNow - timePrev;
  
  #ifdef DEBUG_PRINT
  //Serial.print("time since: "); Serial.println(timePassed);
  Serial.print("d_h: ");Serial.print(headDesired);
  Serial.print("| a_h: "); Serial.print(headCurrent);
  #endif

  if(timePassed > 0){/* Handles wrap of timeNow */
    
    /* PID for Heading */
    int headError = headDiff(headCurrent, headDesired);
    headInteg = headInteg + (headError * (timePassed/1000.));
    headInteg = constrain(headInteg, -10, 10); //note, do not call functions in constrain, will break! (read docs)
    int headDeriv = (headError - prevHeadErr)/(timePassed/1000.);
    int rudderAngle = KP*headError + KI*headInteg + KD*headDeriv ;
    int maxAng =getHardRight();
    int minAng =getHardLeft();
    rudderAngle = constrain(rudderAngle, minAng, maxAng);

    /* Speed */ 
    int motorSpeed;
    if(abs(headError) < 45){
      motorSpeed = fullSpeed;
    }else{ /* Turn a tight corner at half speed to decrease turning circle */
      motorSpeed = halfSpeed; 
    }
    //motorSpeed = constrain(motorSpeed, getMinSpeed() , getMaxSpeed());

    /* Set speed and rudders */
    setRudders(rudderAngle); 
    setMotors(motorSpeed);
   
   
    #ifdef DEBUG_PRINT
    Serial.print("| set_rudders: "); Serial.print(rudderAngle);
    Serial.print("| set_speed: "); Serial.println(motorSpeed);
    #endif

    /* Update values for next iteration */
    prevHeadErr = headError;
  }
  timePrev = timeNow;
  delay(100); //note, any delay inside this loop will delay reading of next values
}
