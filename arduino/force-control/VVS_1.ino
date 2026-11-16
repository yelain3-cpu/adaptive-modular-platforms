#include <Servo.h>  // Include the Servo library for controlling PWM electronic switches
Servo C, X, P;      // Define servo objects C, X, and P for controlling electronic valves and a vacuum pump

int air_delay = 0;  // Initialize an integer variable air_delay to 0 for controlling delay time
float timer = 0;    // Initialize a floating-point variable timer to 0 for timing purposes
float amount = 0;   // Initialize a floating-point variable amount to 0 for keeping track of the amount of action

void setup() {

  Serial.begin(115200);  // Start serial communication at a baud rate of 115200

  pinMode(LED_BUILTIN, OUTPUT);    // Set the built-in LED pin as an output for initialization
  digitalWrite(LED_BUILTIN, LOW);  // Turn off the built-in LED

  C.attach(5, 500, 2500);  // Attach servo C to pin 5 with pulse width limits
  C.write(0);              // Set servo C to position 0 (release air)

  X.attach(7, 500, 2500);  // Attach servo X to pin 7 with pulse width limits
  X.write(0);              // Set servo X to position 0 (exhaust air)

  P.attach(3, 500, 2500);  // Attach servo P to pin 3 with pulse width limits
  P.write(0);              // Set servo P to position 0 (vacuum pump off)

  int fsr = 0;             // Initialize an integer variable fsr to 0 for storing FSR sensor readings
  pinMode(A0, INPUT);      // Set pin A0 as input for reading FSR sensor values

  Serial.begin(9600);      // Start serial communication at a baud rate of 9600
  C.write(0);              // Set servo C to position 0
  X.write(180);            // Set servo X to position 180 (suck in air)
  delay(7000);            // Delay for 10 seconds
  C.write(180);            // Set servo C to position 180 (inflate)
  X.write(0);              // Set servo X to position 0 (exhaust)
  P.write(180);            // Set servo P to position 180 (vacuum pump on)
  delay(5000);            // Delay for another 10 seconds
}

void loop() {

  if (Serial.available()) {
    air_delay = Serial.read();  // Read the air delay value from serial input
  }

  int fsr = analogRead(A0);  // Read the FSR sensor value from pin A0
  Serial.println(fsr);       // Print the FSR sensor value to the serial monitor

  if (fsr > 300 && timer <= 500) {  // Check FSR value and timer conditions

    pump(1, air_delay);  // Call the pump function to inflate with a given delay
    timer++;             // Increment the timer
    amount++;            // Increment the amount
  }

  if (fsr > 300 && timer >= 500) {  // Check FSR value and timer conditions

    pump(2, 1000);  // Call the pump function to stop movement with a given delay
  }

  if (fsr < 300 && amount > 0) {  // Check FSR value and amount condition

    pump(0, 1);  // Call the pump function to release air with a small delay
    amount--;      // Decrement the amount
    if (amount == 200) {
      timer = 0;  // Reset the timer if the amount is 0
      amount = 0;
    }
  }

  if (fsr < 300 && amount == 0) {  // Check FSR value and amount condition

    pump(2, 10);  // Call the pump function to stop movement with a longer delay
  }

  delay(10);  // Delay for a short period to improve simulation performance
}

void pump(int cmd, int tDelay) {
  switch (cmd) {
    case 0:           // Release air
      C.write(0);     // Set servo C to position 0 (release air)
      X.write(180);   // Set servo X to position 180 (suck in air)
      P.write(180);   // Set servo P to position 180 (vacuum pump on)
      delay(tDelay);  // Delay for the specified time
      break;

    case 1:           // Blow air
      C.write(255);   // Set servo C to position 255 (inflate)
      X.write(0);     // Set servo X to position 0 (exhaust)
      P.write(255);   // Set servo P to position 255 (vacuum pump on)
      delay(tDelay);  // Delay for the specified time
      break;

    case 2:           // No movement
      C.write(0);     // Set servo C to position 0
      X.write(0);     // Set servo X to position 0
      P.write(0);     // Set servo P to position 0
      delay(tDelay);  // Delay for the specified time
      break;
  }
}