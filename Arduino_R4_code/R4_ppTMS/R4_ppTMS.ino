// Triggerbox BNC CNC thomas.quettier2@unibo.it 2023

// Pins setting
int LedPin = 13; 
int ConditionPin = 9, TestPin = 8, BioPin = 7;

// Variables setting
int TriggerDuration = 2; // Duration between high and low (ms)
int IPI = 2; // Inter pulse interval (ms)
int test = 4; // Test variable for conditional triggering

// Voltage measurement
int analogVoltage;


void setup() {
  // Pin initialization
  pinMode(LedPin, OUTPUT);
  pinMode(ConditionPin, OUTPUT);
  pinMode(TestPin, OUTPUT);
  pinMode(BioPin, OUTPUT);
  pinMode(A0, INPUT);  // Analog input pin for voltage measurement
  
  // Serial communication initialization
  Serial1.begin(115200); // Set baud rate for Serial1
}

void loop() {
  digitalWrite(LedPin, HIGH); // Turn on LED to indicate Arduino is active
  
  // Check if there's incoming serial data
  if (Serial1.available() > 0) {
    String command = Serial1.readStringUntil('\n'); // Read command until newline
    
    // Update IPI value
    if (command.startsWith("SET,IPI1,")) {
      IPI = command.substring(9).toInt();
      IPI = max(0, IPI - TriggerDuration); // Ensure IPI doesn't go negative
    } 
    // Test pin triggering logic
    else if (command.startsWith("SET,test,")) {
      test = command.substring(9).toInt();
      if (test == 1) {
        triggerPin(TestPin);
      } else if (test == 2) {
        triggerPin(ConditionPin);
      } else if (test == 3) {
        triggerPin(BioPin);
      }
    } 
    // Combined triggering for "1" command
    else if (command == "1") {
      digitalWrite(BioPin, HIGH);
      digitalWrite(ConditionPin, HIGH);
      delay(TriggerDuration);
      digitalWrite(ConditionPin, LOW);
      digitalWrite(BioPin, LOW);
      delay(IPI);
      digitalWrite(TestPin, HIGH);
      delay(TriggerDuration);
      digitalWrite(TestPin, LOW);
    }
    // Voltage measurement for "9" command
    else if (command == "9") {
      digitalWrite(LedPin, LOW); // Turn off LED to indicate Arduino is active
      delay(TriggerDuration);
      digitalWrite(LedPin, HIGH); // Turn on LED to indicate Arduino is active
      analogVoltage = analogRead(A0);  // Read the analog input
      if (analogVoltage < 750) {
        Serial1.println("low");  // Ensure newline is sent
        } else {
          Serial1.println("high");  // Ensure newline is sent
  }
    }
  }
}

// Function to trigger a pin with specified duration
void triggerPin(int pin) {
  digitalWrite(pin, HIGH);
  delay(TriggerDuration);
  digitalWrite(pin, LOW);
}
