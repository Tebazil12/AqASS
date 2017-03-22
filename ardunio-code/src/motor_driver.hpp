void setupMotor(int pin);

/**
 * Take speed in m/s and driver motors at this
 * speed.
 *
 */
void setMotors(int speed);

void stopMotors();

int getMaxSpeed();

int getMinSpeed();

int getStopSpeed();
