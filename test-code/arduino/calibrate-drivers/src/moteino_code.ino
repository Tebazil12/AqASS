#include <Arduino.h>
#include <avr/sleep.h>
#include "../../../../ardunio-code/src/motor_driver.cpp" //TODO find way to use .hpp files!
#include "../../../../ardunio-code/src/rudder_driver.cpp"
#include "../../../../ardunio-code/src/compass_driver.cpp"
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
    centerRudders();
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


/* ***********************MAIN CODE************************************** */
void setup() {
  initializeCompass();
  setupRudder(PIN_RUDDERS);
  setupMotor(PIN_MOTORS);
  timePrev = millis();
}

void loop(){
  Serial.println("loop");

  /* Refresh value */
  headingCurrent = getCompass();
  Serial.print("Heading: "); Serial.println(headingCurrent);
  unsigned long timeCurrent = millis(); //put in wrap handling, just in case
  int timePassed = timeCurrent - timePrev;
  Serial.print("time passed: "); Serial.println(timePassed);

  /* Rudder Test - Rudder to hard left */
  for(int i = getCenter(); i < getHardLeft(); i++){
    rudderAngle = i;
    setRudders(rudderAngle);
    delay(100);
  }
  centerRudders();
  delay(1000);
  /* Rudder Test - Rudder to hard right */
  for(int i=getCenter(); i<getHardRight(); i--){
    rudderAngle = i;
    setRudders(rudderAngle);
    delay(100);
  }
  centerRudders();

  delay(10000);


  /* Update values for next iteration */
  timePrev = timeCurrent;
  delay(100);
}
//#endif
