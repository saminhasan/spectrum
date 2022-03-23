// Include the AccelStepper library:
#include <AccelStepper.h>
#include "SerialTransfer.h"

SerialTransfer myTransfer;
// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1

// Define a stepper and the pins it will use
// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

long position = 0;


// Example 3 - Receive with start- and end-markers

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);  
    // Change these to suit your stepper if you want
  stepper.setMaxSpeed(100);
  stepper.setAcceleration(50);
  //stepper.moveTo(500);


}

void loop()
{
    // If at the end of travel go to the other end
  if(myTransfer.available())
  {
    // use this variable to keep track of how many
    // bytes we've processed from the receive buffer
    uint16_t recSize = 0;
    recSize = myTransfer.rxObj(position, recSize);
  }
    stepper.moveTo(position);

    stepper.run();
   /* 
   Serial.print(" currentPosition : ");
   Serial.print(stepper.currentPosition());
   Serial.print("  | ");
   Serial.print(" targetPositio : ");
   Serial.print(stepper.targetPosition());
   Serial.print("  | ");
   Serial.print(" speed : ");
   Serial.print(stepper.speed());
   Serial.println();
   */
}


void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        Serial.print("This just in ... ");
        Serial.println(receivedChars);
        newData = false;
    }
}
