// Include the AccelStepper library:
#include <AccelStepper.h>
#include "SerialTransfer.h"

SerialTransfer myTransfer;
// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 2
#define stepPin 3
#define enPin 4
#define motorInterfaceType 1

// Define a stepper and the pins it will use
// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

long position = 0;


struct STRUCT {
    long acceleration = 100.0;
    long maxspeed = 100.0;
    long position = 0;
    long uplimit = 0;
    long lowlimit = 0;
    bool stop = true;
    bool set_param = false;
} testStruct;

void setup()
{
  Serial.begin(115200);
    Serial1.begin(115200);

  myTransfer.begin(Serial);  
    // Change these to suit your stepper if you want
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(100);
  //stepper.moveTo(500);
pinMode(enPin,OUTPUT);

}

void loop()
{
    // If at the end of travel go to the other end
  if(myTransfer.available())
  {
    // use this variable to keep track of how many
    // bytes we've processed from the receive buffer
    uint16_t recSize = 0;
    recSize = myTransfer.rxObj(testStruct, recSize);
  }
debug_print();
    
if(!testStruct.stop)
{digitalWrite(enPin, LOW);

  if (testStruct.set_param)
  {
  stepper.setAcceleration(testStruct.acceleration);
    stepper.setMaxSpeed(testStruct.maxspeed);

   }
   /*

if(testStruct.position  > testStruct.lowlimit && testStruct.position < testStruct.uplimit)
   
   */
   if(true){
    stepper.moveTo(testStruct.position);
    stepper.run();
   }
}

  else
digitalWrite(enPin, HIGH);
}

void debug_print()
{
  Serial1.print(testStruct.acceleration);
  Serial1.print(", ");
    Serial1.print(testStruct.maxspeed);
  Serial1.print(", ");
    Serial1.print(testStruct.position);
  Serial1.print(", ");
    Serial1.print(testStruct.uplimit);
  Serial1.print(", ");
  Serial1.print(testStruct.lowlimit);
  Serial1.print(". ");
    Serial1.print(testStruct.stop);
  Serial1.print(". ");
    Serial1.print(testStruct.set_param);
  Serial1.print(". ");
  Serial1.println();
}
