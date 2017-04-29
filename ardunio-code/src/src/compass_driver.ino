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

/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

/** 
 * Initialize compass. This is adapted from the examples given in the
 * HMC5883L library. 
 */
void initCompass(){
#ifdef DEBUG_PRINT
  Serial.println("HMC5883 Magnetometer Test");
  Serial.println("");
#endif

  /* Initialise the sensor */
  if(!mag.begin())
  {
    /* There was a problem detecting the HMC5883 ... check your connections */
#ifdef DEBUG_PRINT
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while(1) Serial.println("oh no!");
#endif
  }
}

/**
 * Request value from compass. This is adapted from the examples given in the
 * HMC5883L library.
 *
 * @return current compass heading as int
 */
int getCompass(){
  /* Get a new sensor event */
  sensors_event_t event;
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.y, event.magnetic.x);

  // Once you have your heading, you must then add your 'Declination Angle', 
  // which is the 'Error' of the magnetic field in your location.
  // Find yours here: http://www.magnetic-declination.com/
  // Mine is: -13* 2' W, which is ~13 Degrees, or (which we need) 0.22 radians
  // If you cannot find your Declination, comment out these two lines, 
  //your compass will be slightly off.
  float declinationAngle = 0.035;
  heading += declinationAngle;

  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;

  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;

  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI;


  if( headingDegrees >= (330)){
    headingDegrees = headingDegrees -360;
  }

  headingDegrees = ((9.2583518*pow(10, -8)) * pow(headingDegrees, 4)) - (0.000064623 *pow(headingDegrees, 3)) + (0.0112157562*pow(headingDegrees, 2)) + (1.0274992414*headingDegrees) + 23.89831;

  return int(headingDegrees); //this returns an int
  // return 56;
}

