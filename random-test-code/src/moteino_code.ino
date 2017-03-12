#include <Arduino.h>
#include "motor_driver.h"
#include "rudder_driver.h"
#include "compass_driver.h"
#include "serial_comms.h"

//#define UNIT_TEST
#define MAX_SERIAL_IN 9

int desiredHeading;
int motorSpeed; // in m/s
int rudderAngle; // in degrees
int currentHeading; // in degrees (min 0, max 359)
unsigned long prevTime;

/* ***********************FUNCTIONS************************************** */

void serialEvent(){
  //when theres incoming serial, do this
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine);

  switch (nextLine[0]) {
  case 'c':
    // Serial.println("you said c!");
    Serial.println(currentHeading);//probably need a better procedure than this
    //is that really the best thing? instead of calling getCompass?
    break;
  case 'h':
    int newHeading;//find the number
    desiredHeading = newHeading;

  }
  Serial.print("Current Command:");
  Serial.println(nextLine);
  Serial.println("END_AGAIN");
}

/**
 * Read in next line of serial (up to a newline or carriage return) one
 * char at a time, and save them to thisLine.
 *
 * @param thisLine where read in command will be stored
 */
void readSerialLine(char* thisLine){
  int available = Serial.available();
  int index;
  for(index = 0; index < available; index++){
    if(index >= MAX_SERIAL_IN){
      break;
    }
    else{
      Serial.println("in");
      char c = Serial.read();
      Serial.print("c: ");
      Serial.println(c);
      if(c == '\n' || c == '\r'){
        thisLine[index] = '\0';
        break;
      }
      else{
        thisLine[index] = c;
      }
    }
  }
  thisLine[index] = '\0';
  Serial.println("END");
}

int wrapHeading(int angle){
  while(angle < 0){ //this seems a little slow/ineligant?
    angle += 360;
  }
  angle = angle % 360;
  return angle;
}

#ifdef UNIT_TEST
/* ***************************TESTS************************************** */
#include <avr/sleep.h> //maybe move this later if used in maincode!
#include "tests.h"

void setup() {
    delay(2000); //as suggested when using Unity
    Serial.begin(9600);
}

void loop() {
  runTests();
}

#else
/* ***********************MAIN CODE************************************** */
void setup() {
  initializeCompass();
  prevTime = millis();
  //set desiredHeading to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
}

void loop(){
  Serial.println("loop");
  currentHeading = getCompass();

  //do some pid stuff here
  unsigned int currentTime = millis();
  int time_since = currentTime - prevTime;
  Serial.print("time since: ");
  Serial.println(time_since);

//  headingError = currentHeading - //


  setRudders(rudderAngle); //rename this to turn(angle) ? to make this based on angle of boat instead of rudders? (in this case those are ==)
  setMotors(motorSpeed); //rename this to setSpeed(speed) ? so then the driver handles motor speeds

  delay(1000);// obviously, reduce this
  //note, any delay inside this loop will delay reading of next values/
  // requests from pi

  prevTime = currentTime;
}
#endif
