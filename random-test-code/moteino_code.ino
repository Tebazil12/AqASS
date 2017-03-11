#define MAX_SERIAL_IN 9

int desiredHeading;
int motorSpeed;//will this be in m/s then converted? clever changing ratio depending on winds, drag etc?
int rudderAngle;
int currentCompass;

void setup() {
  Serial.begin(9600);
  //set desiredHeading to be initial heading when turned on (?)
  //find central positions for the rudder, and nice start speed for the motors
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

/**
 * Request value from compass.
 *
 * @return current compass heading
 */
int getCompass(){

}

void setRudders(int angle){

}

void setMotors(int speed){

}

void loop(){
  Serial.println("loop");
  currentCompass = getCompass();

  //do some pid stuff here

  setRudders(rudderAngle);
  setMotors(motorSpeed);

  delay(1000);// obviously, reduce this
}


void serialEvent(){
  //when theres incoming serial, do this
  char nextLine[MAX_SERIAL_IN+1];
  readSerialLine(nextLine);

  switch (nextLine[0]) {
  case 'c':
    // Serial.println("you said c!");
    Serial.println(currentCompass);//probably need a better procedure than this
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




