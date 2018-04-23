#define potPin    A0
#define enA       2
#define in1       6
#define in2       7

void setup() {
    Serial.begin(9600);
    pinMode(potPin, INPUT);
    pinMode(enA, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
}

void loop() {
  Serial.println(analogRead(potPin));
//  Lumpy();
//  SlideToValue(300);
//  delay(600);
  SlideToValue(850);
//  delay(600);
}

void Lumpy(){
    int val = analogRead(potPin);
    for(int i = 0; i<1024; i+= 200){
       if(val >  i-50 && val < i+50){
          if(val < i+3){
              digitalWrite(enA, HIGH);
              digitalWrite(in1, LOW); digitalWrite(in2, HIGH); 
//              analogWrite(enA, 120);
          }else if(val > i-3){
              digitalWrite(enA, HIGH);
              digitalWrite(in1, HIGH); digitalWrite(in2, LOW); 
//              analogWrite(enA, 120);
          }else{
//              analogWrite(enA, LOW);
                digitalWrite(enA, LOW);
          }
       }
       delay(100);
    }
}
//
void SlideToValue(int targetValue){
  int val = analogRead(potPin);
  if(abs(val - targetValue) > 20){
      if(val > targetValue){
          digitalWrite(in1, LOW);
          digitalWrite(in2, HIGH); 
      }else{
          digitalWrite(in1, HIGH);
          digitalWrite(in2, LOW); 
      }
      analogWrite(enA, max(min(abs(val - targetValue), 255), 200));
  }else{
      // Turn off motor
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);  
      analogWrite(enA, 0);
  }
}
