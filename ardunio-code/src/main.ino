#include <Arduino.h>
#include <avr/sleep.h>
#include "motor_driver.hpp"
#include "rudder_driver.hpp"
#include "compass_driver.hpp"
//#include "serial_comms.h"

//#define UNIT_TEST

#define MAX_SERIAL_IN 9

#define PIN_MOTORS 9
#define PIN_RUDDERS 8

//TODO change to be different for speed and heading!
#define H_KU 0.1 //TODO must experiment and change
#define H_TU 1 //TODO must experiment and change
#define H_KP (0.6*H_KU) //Ziegler–Nichols method
#define H_KI (1.2*H_KU/H_TU) //Ziegler–Nichols method
#define H_KD (3*H_KU*H_TU/40) //Ziegler–Nichols method

#define S_KU 0.01 //TODO must experiment and change
#define S_TU 1 //TODO must experiment and change
#define S_KP (0.6*H_KU) //Ziegler–Nichols method
#define S_KI (1.2*H_KU/H_TU) //Ziegler–Nichols method
#define S_KD (3*H_KU*H_TU/40) //Ziegler–Nichols method

//TODO check if default values make sense

int headingDesired = 0;
int headingCurrent; // in degrees (min 0, max 359)
int prevHeadErr = 0;
int headingInteg = 0;
int headingBias = 0;

int speedBase = 0; //TODO adjust this
int speedDesired = 0;
int speedCurrent; //in m/s - this will only be updated when the pi tells it new info
int speedInteg = 0;//TODO must remember to reset when wildly different desired values
int prevSpeedErr = 0;

int motorSpeed = 0; // in m/s //do these really need to be global?
int rudderAngle =0; // in degrees //do these really need to be global?

int compassOffset = 0;

unsigned long timePrev;

/* ***********************FUNCTIONS************************************** */

int getNumber(char* nextLine){
  int number;
  if(nextLine[3] == ')'){//TODO change this back to not using brackets?
    /* If in the format h(5) */
    number = nextLine[2]-'0';
  }
  else if(nextLine[4] == ')'){
    /* If in format h(56) */
    number = ((nextLine[2]-'0')*10) + (nextLine[3]-'0');
  }
  else{
    /* If in format h(256) */
    number = ((nextLine[2]-'0')*100) + ((nextLine[3]-'0')*10) + (nextLine[4]-'0');
  }
  return number;
}

/* when theres incoming serial, do this */
void serialEvent(){
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine);
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
    speedDesired = temp;
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
    //  Serial.println("in");
      char c = Serial.read();
    //  Serial.print("c: "); Serial.println(c);
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
//  Serial.println("END");
}

/* Make sure angle is greater than or equal to 0 and less than 360 */
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
  headingDesired = 90;
  speedDesired =100;
  //set headingDesired to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
}

void loop(){
  //Serial.println("loop");
  Serial.print("d_h: ");Serial.print(headingDesired);


  /* Refresh value */
  headingCurrent = getCompass() - compassOffset;
  Serial.print("| a_h: "); Serial.print(headingCurrent);
  unsigned long timeCurrent = millis();
  int timePassed = timeCurrent - timePrev;
  //Serial.print("time since: "); Serial.println(timePassed);

  /* Handles wrapping of timeCurrent */
  if(timePassed > 0){
    /* PID for Heading */
    int error1 = headingDesired - headingCurrent; //headingError will be negative when boat needs to turn anticlockwise, and positive when it needs to turn clockwise
  //  int error2 = headingCurrent - headingDesired;
    int headingError;
    if(abs(error2) < abs(error1)){
      headingError = error2;
    }else{
      headingError = error1;
    }
    if(headingInteg >100) headingInteg = 100;
    else headingInteg = headingInteg + (headingError * (timePassed/1000));
    int headingDeriv = (headingError - prevHeadErr)/(timePassed/1000);
    rudderAngle = H_KP*headingError + H_KI*headingInteg + H_KD*headingDeriv + headingBias;//bias could be used on the fly to correct for crabbing of boat?
    if(rudderAngle>90) rudderAngle = 90;
    else if(rudderAngle<-90) rudderAngle =-90;

    /* PID for Speed */
    int speedError = speedDesired - speedCurrent; //headingError will be negative when boat needs to turn anticlockwise, and positive when it needs to turn clockwise
    speedInteg = speedInteg + (speedError *(timePassed/1000));//DON'T USE TIME PASSED WHEN ITS NOT UPDATED EVERY LOOP!
    int speedDeriv = (speedError - prevSpeedErr)/(timePassed/1000);
    motorSpeed = S_KP*speedError + S_KI*speedInteg + S_KD*speedDeriv;// + speedBase;
    if(motorSpeed>180) motorSpeed = 180;
    else if(motorSpeed<-80) motorSpeed = -80;

    /* Set speed and rudders */
    setRudders(rudderAngle); //rename this to H_TUrn(angle) ? to make this based on angle of boat instead of rudders? (in this case those are ==)
    setMotors(motorSpeed); //rename this to setSpeed(speed) ? so then the driver handles motor speeds
    Serial.print("| set_rudders: "); Serial.print(rudderAngle);

    Serial.print("|| d_s: ");Serial.print(speedDesired);
    Serial.print("| a_s: ");Serial.print(speedCurrent);
    Serial.print("| set_speed: "); Serial.println(motorSpeed);

    /* Update values for next iteration */
    prevHeadErr = headingError;
  }
  timePrev = timeCurrent;
  delay(1000);// obviously, reduce this //note, any delay inside this loop will delay reading of next values/
}
//#endif
