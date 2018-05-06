int potPin[] = {A0, A1, A2, A3, A4};
int in1[] = {8, 10, 12, 14, 16};
int in2[] = {9, 11, 13, 15, 17};
int en[] = {2, 3, 4, 5, 6};
int pinCount = 5;
int motorCount = 5;
int thisValue = 0;
int targetValue[5];

void setup() {
    Serial.begin(9600);

    // initialize
    for (int thisPin = 0; thisPin < pinCount; thisPin++) {
      pinMode(potPin[thisPin], INPUT);
      pinMode(in1[thisPin], OUTPUT);
      pinMode(in2[thisPin], OUTPUT);
      pinMode(en[thisPin], OUTPUT);
    }

    for (int initValue = 0; initValue < motorCount; initValue++){
      targetValue[initValue] = 200;
    }

    SlideToValue(targetValue);
}

void loop() {
  
  // get data from serial
  if(Serial.available()){ // only send data back if data has been sent
    char inByte = Serial.read(); // read the incoming data
    Serial.print("The number is ");
    Serial.println(inByte); // send the data back in a new line so that it is not all one long line
    targetValue[thisValue] = int(inByte)*4 + 240;
    thisValue ++;
  }

  // pass value to targetValue
  SlideToValue(targetValue);

  // reset index
  if (thisValue == 5) {
    thisValue = 0;
  }
}

void SlideToValue(int targetValue[]){

  // check each slider
  for (int thisMotor = 0; thisMotor < motorCount; thisMotor++){
    int val = analogRead(potPin[thisMotor]);
    if(abs(val - targetValue[thisMotor]) > 10){
      digitalWrite(en[thisMotor], HIGH);
        if(val > targetValue[thisMotor]){
            digitalWrite(in1[thisMotor], LOW);
            digitalWrite(in2[thisMotor], HIGH); 
        }else{
            digitalWrite(in1[thisMotor], HIGH);
            digitalWrite(in2[thisMotor], LOW); 
        }
//        analogWrite(en[thisMotor], max(min(abs(val - targetValue[thisMotor]), 255), 200));
    }else{
        // Turn off motor
        digitalWrite(in1[thisMotor], LOW);
        digitalWrite(in2[thisMotor], LOW);  
        digitalWrite(en[thisMotor], LOW);
//        analogWrite(en[thisMotor], 0);
    }
   }
}
