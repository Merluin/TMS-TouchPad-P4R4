const int ledPin = 13; // Define the LED pin as 13

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin as an output
  Serial.begin(9600);     // Initialize serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read(); // Read the incoming character from serial

    if (receivedChar == '1') {
      digitalWrite(ledPin, HIGH); // Turn on the LED
      delay(1000);               // Wait for 1 second
      digitalWrite(ledPin, LOW);  // Turn off the LED
    }
  }
}
