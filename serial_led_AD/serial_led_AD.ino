const int ledPin = 7; // Define the LED pin as 13

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin as an output
}

void loop() {
      digitalWrite(ledPin, HIGH); 
      delay(1);
      digitalWrite(ledPin, LOW);  // Turn off the LED
      delay(1000);
}
