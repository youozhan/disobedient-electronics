//#include <ArduinoJson.h>

//Reference
//https://learn.adafruit.com/mini-thermal-receipt-printer/bitmap-printing
//https://www.arduino.cc/en/Tutorial/Button

#include "Adafruit_Thermal.h" 
#include "SoftwareSerial.h"
#define TX_PIN 6 // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define RX_PIN 5 // Arduino receive   GREEN WIRE   labeled TX on printer 

//#define FIREBASE_HOST "prediction-bd050.firebaseio.com"
//#define FIREBASE_AUTH

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);     // Pass addr to printer constructor

// constants won't change. They're used here to set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledRed =  12;      // the number of the LED pin
const int ledGreen =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int value = 0;

// -----------------------------------------------------------------------

void setup() {
  // connect to Firebase
//  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  
  // initialize the LED pin as an output:
  pinMode(ledRed, OUTPUT);
  pinMode(ledGreen, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  
  // This line is for compatibility with the Adafruit IotP project pack,
  // which uses pin 7 as a spare grounding point.  You only need this if
  // wired up the same way (w/3-pin header into pins 5/6/7):
  pinMode(7, OUTPUT); digitalWrite(7, LOW);

  // NOTE: SOME PRINTERS NEED 9600 BAUD instead of 19200, check test page.
  mySerial.begin(19200);  // Initialize SoftwareSerial
  printer.begin();        // Init printer (same regardless of serial type)

}

void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

//  value = Serial.read();
//  printer.println(value); 

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
    // turn LED on:
    digitalWrite(ledRed, HIGH);
    delay(1000);
    digitalWrite(ledRed, LOW);
    delay(1000);
    digitalWrite(ledGreen, HIGH);
    delay(1000);

    // get value
//    printer.println(F(Firebase.getFloat("predictions"));   
    printer.println(F("Firebase test"));  
    
    printer.feed(2);

    printer.sleep();      // Tell printer to sleep
    delay(3000L);         // Sleep for 3 seconds
    printer.wake();       // MUST wake() before printing again, even if reset
    printer.setDefault(); // Restore printer to defaults
    digitalWrite(ledGreen, LOW);
  }
}
