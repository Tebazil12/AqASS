#include <Arduino.h>
#include <avr/sleep.h>
#include "motor_driver.h"
#include "rudder_driver.h"
#include "compass_driver.h"
//#include "serial_comms.h"

//#define UNIT_TEST

#define MAX_SERIAL_IN 9

#define PIN_MOTORS 9
#define PIN_RUDDERS 8

#define KU 5 //TODO must experiment and change
#define TU 1 //TODO must experiment and change
#define KP (0.6*KU) //Ziegler–Nichols method
#define KI (1.2*KU/TU) //Ziegler–Nichols method
#define KD (3*KU*TU/40) //Ziegler–Nichols method

int headingDesired;
int headingCurrent; // in degrees (min 0, max 359)
int prevHeadErr = 0;
int headingInteg = 0;
int headingBias = 0;

int speedDesired;
int speedCurrent; //in m/s - this will only be updated when the pi tells it new info
int speedInteg = 0;//must remember to reset when wildly different desired values
int prevSpeedErr = 0;

int motorSpeed; // in m/s //do these really need to be global?
int rudderAngle; // in degrees //do these really need to be global?

unsigned long timePrev;

/* ***********************FUNCTIONS************************************** */

/* when theres incoming serial, do this */
void serialEvent(){
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine);
  switch (nextLine[0]) {
  /* Send current heading */
  case 'c':
    Serial.print("c");Serial.println(headingCurrent); //is that really the best thing? instead of calling getCompass?
    break;

  /* Update the desiredHeading */
  case 'h':
    if(nextLine[2] == '\n'){
      /* If in the format h5 */
      headingDesired = nextLine[1];
    }else if(nextLine[3] == '\n'){
      /* If in format h56 */
      headingDesired = (nextLine[1]*10) + nextLine[2];
    }else{
      /* If in format h256 */
      headingDesired = (nextLine[1]*100) + (nextLine[2]*10) + nextLine[3];
    }
    break;

  /* Update desiredSpeed */
  case 'm':
    break;

    //add case for setting compass ofset?
  /* End everything, shutdown */
  case 'e':
    stopMotors();
    stopRudders();
    Serial.write('e');
    delay(100); // to allow time for serial to print
    cli();
    sleep_enable();
    sleep_cpu(); // check this does sleep and never wakes up
    break;
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
  initializeCompass();
  setupRudder(PIN_RUDDERS);
  setupMotor(PIN_MOTORS);
  timePrev = millis();
  //set headingDesired to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
}

void loop(){
  Serial.println("loop");

  /* Refresh value */
  headingCurrent = getCompass(); //think about boat heading being off by a small amount due to not moving directly forward
  Serial.print("Heading: "); Serial.println(headingCurrent);
  unsigned long timeCurrent = millis(); //put in wrap handling, just in case
  int timePassed = timeCurrent - timePrev;
  Serial.print("time since: "); Serial.println(timePassed);

  rudderAngle = 90;
  motorSpeed = 110;

  /* Set speed and rudders */
  setRudders(rudderAngle); //rename this to turn(angle) ? to make this based on angle of boat instead of rudders? (in this case those are ==)
  setMotors(motorSpeed); //rename this to setSpeed(speed) ? so then the driver handles motor speeds

  /* Update values for next iteration */
  timePrev = timeCurrent;
  delay(100);// obviously, reduce this //note, any delay inside this loop will delay reading of next values/
}
//#endif
