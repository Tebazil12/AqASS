#include <Wire.h>
#include "SFE_HMC6343.h"
SFE_HMC6343 compass;

void initializeCompass(){
  Serial.begin(115200);
  // Give the HMC6343 a half second to wake up
  delay(500);

  // Initialize the HMC6343 and verify its physical presence
  if (!compass.init()){
    Serial.println("Sensor Initialization Failed\n\r"); // Report failure, is the sensor wiring correct?
  }
}

/**
 * Request value from compass.
 *
 * @return current compass heading as int
 */
int getCompass(){
  compass.readHeading();
  Serial.println(compass.heading);
  return compass.heading; //this returns an int
}
