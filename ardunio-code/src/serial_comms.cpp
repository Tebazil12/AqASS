#include <Arduino.h>


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



/**
 * Read in next line of serial (up to a newline or carriage return) one
 * char at a time, and save them to thisLine.
 *
 * @param thisLine where read in command will be stored
 */
void readSerialLine(char* thisLine, int MAX_SERIAL_IN){//builds on functions in abersailbot/dewi-arduino
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
