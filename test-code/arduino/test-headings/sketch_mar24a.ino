
void setup(){
  Serial.begin(9600);
  boolean fail = false;
  for(int i =0; i <=36;i++){
    int desired = i*10;
    for(int j =0; j <=36;j++){
      int current = j*10;
      int m;

      int first = (360-desired)+current;
      int second = desired-current;
      int third = (360-current)+desired;

      if(abs(first)<=abs(second) && abs(first)<=abs(third)){
        m = first;
      }
      else if (abs(second)<=abs(first) && abs(second) <=abs(third)){
        m = second;
      }
      else if (abs(third)<=abs(first) && abs(third)<=abs(second)){
        m = third;
      }
      else{
        Serial.print("This should be impossible, what did you do?!");
      }
      
      if(abs(m) >180) fail = true;
      Serial.print("desired: ");
      Serial.print(desired);
      Serial.print(" current: ");
      Serial.print(current);
      Serial.print(" m: ");
      Serial.println(m);

    }
  }
  Serial.println(true);
  Serial.println(false);
  Serial.println(fail);
}

void loop(){

}


