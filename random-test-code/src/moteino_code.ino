#include <Arduino.h>
#include "motor_driver.h"
#include "rudder_driver.h"
#include "compass_driver.h"
//#include "serial_comms.h"

//#define UNIT_TEST
#define MAX_SERIAL_IN 9
#define KU
#define TU
#define KP (0.6*KU) //Ziegler–Nichols method
#define KI (1.2*KU/TU) //Ziegler–Nichols method
#define KD (3*KU*TU/40) //Ziegler–Nichols method

int headingDesired;
int motorSpeed; // in m/s
int rudderAngle; // in degrees
int headingCurrent; // in degrees (min 0, max 359)
int speedCurrent; //in m/s - this will only be updated when the pi tells it new info
unsigned long timePrev;
int headingInteg = 0;


/* ***********************FUNCTIONS************************************** */

void serialEvent(){
  //when theres incoming serial, do this
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine);

  switch (nextLine[0]) {
  case 'c':
    // Serial.println("you said c!");
    Serial.println(headingCurrent);//probably need a better procedure than this
    //is that really the best thing? instead of calling getCompass?
    break;
  case 'h':
    int newHeading;//find the number
    headingDesired = newHeading;

    //add case for setting compass ofset?

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
void readSerialLine(char* thisLine){//builds on functions in abersailbot/dewi-arduino
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
  setupRudder();
  timePrev = millis();
  //set headingDesired to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
}

void loop(){
  Serial.println("loop");
  headingCurrent = getCompass(); //think about boat heading being off by a small amount due to not moving directly forward
  Serial.print("Heading: ");
  Serial.println(headingCurrent);
  //do some pid stuff here
  unsigned long timeCurrent = millis();
  int timePassed = timeCurrent - timePrev;
  Serial.print("time since: ");
  Serial.println(timePassed);

  headingError = headingDesired - headingCurrent; //headingError will be negative when boat needs to turn anticlockwise, and positive when it needs to turn clockwise
  headingInteg = headingInteg + (headingError * timePassed);
  int headingDeriv = (headingError - prevHeadErr)/timePassed;
  rudderAngle = KP*headingError + KI*headingInteg + KD*headingDeriv + bias;//bias could be used on the fly to correct for crabbing of boat?

  speedError = speedDesired - speedCurrent; //headingError will be negative when boat needs to turn anticlockwise, and positive when it needs to turn clockwise
  speedInteg = speedInteg + (speedError * timePassed);
  int speedDeriv = (speedError - prevSpeedErr)/timePassed;
  motorSpeed = KP*speedError + KI*speedInteg + KD*speedDeriv + bias;

  setRudders(rudderAngle); //rename this to turn(angle) ? to make this based on angle of boat instead of rudders? (in this case those are ==)
  setMotors(motorSpeed); //rename this to setSpeed(speed) ? so then the driver handles motor speeds

  delay(1000);// obviously, reduce this
  //note, any delay inside this loop will delay reading of next values/
  // requests from pi
  prevHeadErr = headingError;
  timePrev = timeCurrent;
}
#endif
