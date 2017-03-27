
void setupRudder(int pin);

/**
 * This should correspond to the angle you want the rudders set at,
 * with 0 setting the boat to go straight forward, -90 should turn the
 * boat fully to the left, and 90 should turn the boat fully to the right.
 */
void setRudders(int angle);

/* Covert from what the main code expects (angle of rudder in degrees) to raw rudder values */
int softToDeg(int angle);

/* Covert from raw rudder values to what the main code expects (angle of rudder in degrees) */
int rawToDeg(int value);

void stopRudders();

int getHardLeft();

int getHardRight();

int getCenter();
