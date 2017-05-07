void test_wrapp_heading(void) {
    Serial.print("heading-wrapping ");
    boolean pass = true;
    delay(100);
    if(wrapHeading(200) == 200) Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(360) == 0)   Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(0) == 0)     Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(361) == 1)   Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(-1) == 359)  Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(-361) == 359)Serial.print("."); else {Serial.print("F "); pass = false;}
    if(wrapHeading(721) == 1)   Serial.print("."); else {Serial.print("F "); pass = false;}
    if(pass) Serial.println("PASS"); else Serial.println("FAIL");
}

void runTests(){
  Serial.println("=== STARTING TESTS ===");
  test_wrapp_heading();
  // add more tests here
  Serial.println("=== TESTS COMPLETE ===");
  delay(100);
  cli();
  sleep_enable();
  sleep_cpu();
}

/* To run tests above, replace the setup() and void() functions in src.ino with this code */
//
// #include "tests.h"
//
// void setup() {
//     delay(2000); // give time to wake up
//     Serial.begin(9600);
// }
//
// void loop() {
//   runTests();
// }